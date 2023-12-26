import argparse
import fcntl
import logging
import os
import signal
from os.path import join
from threading import Condition, RLock
from threading import Event as TEvent
from threading import Lock
from time import sleep
from typing import Sequence, cast

import pkg_resources

from .logging import set_log_plugin, setup_logger, update_log_plugins
from .plugins import (
    Config,
    Emitter,
    Event,
    HHDAutodetect,
    HHDPlugin,
    load_relative_yaml,
)
from .plugins.settings import (
    get_default_state,
    load_profile_yaml,
    load_state_yaml,
    merge_settings,
    save_profile_yaml,
    save_state_yaml,
    validate_config,
)
from .utils import expanduser, fix_perms, get_context

logger = logging.getLogger(__name__)

CONFIG_DIR = os.environ.get("HHD_CONFIG_DIR", "~/.config/hhd")

ERROR_DELAY = 5
POLL_DELAY = 2
MODIFY_DELAY = 0.1


class EmitHolder(Emitter):
    def __init__(self, condition: Condition) -> None:
        self._events = []
        self._condition = condition

    def __call__(self, event: Event | Sequence[Event]) -> None:
        with self._condition:
            if isinstance(event, Sequence):
                self._events.extend(event)
            else:
                self._events.append(event)
            self._condition.notify_all()

    def get_events(self, timeout: int = -1):
        with self._condition:
            if not self._events and timeout != -1:
                self._condition.wait()
            ev = self._events
            self._events = []
            return ev

    def has_events(self):
        with self._condition:
            return bool(self._events)


def notifier(ev: TEvent, cond: Condition):
    def _inner(sig, frame):
        with cond:
            ev.set()
            cond.notify_all()

    return _inner


def main():
    parser = argparse.ArgumentParser(
        prog="HHD: Handheld Daemon main interface.",
        description="Handheld Daemon is a daemon for managing the quirks inherent in handheld devices.",
    )
    parser.add_argument(
        "-u",
        "--user",
        default=None,
        help="The user whose home directory will be used to store the files (~/.config/hhd).",
        dest="user",
    )
    args = parser.parse_args()
    user = args.user

    # Setup temporary logger for permission retrieval
    ctx = get_context(user)
    if not ctx:
        print(f"Could not get user information. Exiting...")
        return

    detectors: dict[str, HHDAutodetect] = {}
    plugins: dict[str, Sequence[HHDPlugin]] = {}
    cfg_fds = []

    # HTTP data
    https = None
    prev_http_cfg = None

    try:
        set_log_plugin("main")
        setup_logger(join(CONFIG_DIR, "log"), ctx=ctx)

        for autodetect in pkg_resources.iter_entry_points("hhd.plugins"):
            detectors[autodetect.name] = autodetect.resolve()

        logger.info(f"Found plugin providers: {', '.join(list(detectors))}")

        logger.info(f"Running autodetection...")
        for name, autodetect in detectors.items():
            plugins[name] = autodetect([])

        plugin_str = "Loaded the following plugins:"
        for pkg_name, sub_plugins in plugins.items():
            plugin_str += (
                f"\n  - {pkg_name:>8s}: {', '.join(p.name for p in sub_plugins)}"
            )
        logger.info(plugin_str)

        # Get sorted plugins
        sorted_plugins: Sequence[HHDPlugin] = []
        for plugs in plugins.values():
            sorted_plugins.extend(plugs)
        sorted_plugins.sort(key=lambda x: x.priority)

        if not sorted_plugins:
            logger.error(f"No plugins started, exiting...")
            return

        # Open plugins
        lock = RLock()
        cond = Condition(lock)
        apply_cond = Condition(lock)
        emit = EmitHolder(cond)
        for p in sorted_plugins:
            set_log_plugin(getattr(p, "log") if hasattr(p, "log") else "ukwn")
            p.open(emit, ctx)
            update_log_plugins()
        set_log_plugin("main")

        # Compile initial configuration
        hhd_settings = {"hhd": load_relative_yaml("settings.yml")}
        settings = merge_settings(
            [*[p.settings() for p in sorted_plugins], hhd_settings]
        )
        state_fn = expanduser(join(CONFIG_DIR, "state.yml"), ctx)
        token_fn = expanduser(join(CONFIG_DIR, "token"), ctx)

        # Load profiles
        profiles = {}
        templates = {}
        conf = get_default_state(settings)
        profile_dir = expanduser(join(CONFIG_DIR, "profiles"), ctx)
        os.makedirs(profile_dir, exist_ok=True)
        fix_perms(profile_dir, ctx)

        # Monitor config files for changes
        should_initialize = TEvent()
        should_initialize.set()
        should_exit = TEvent()
        signal.signal(signal.SIGPOLL, notifier(should_initialize, cond))
        signal.signal(signal.SIGINT, notifier(should_exit, cond))
        signal.signal(signal.SIGTERM, notifier(should_exit, cond))

        while not should_exit.is_set():
            #
            # Configuration
            #

            # Initialize if files changed
            if should_initialize.is_set():
                set_log_plugin("main")
                logger.info(f"Reloading configuration.")
                new_conf = load_state_yaml(state_fn, settings)
                if not new_conf:
                    logger.warning(f"Using previous configuration.")
                else:
                    conf = new_conf
                profiles = {}
                templates = {}

                for fn in os.listdir(profile_dir):
                    if not fn.endswith(".yml"):
                        continue
                    name = fn.replace(".yml", "")
                    s = load_profile_yaml(join(profile_dir, fn))
                    if s:
                        validate_config(s, settings, use_defaults=False)
                        if name.startswith("_"):
                            templates[name] = s
                        else:
                            # Profiles are shared so lock when accessing
                            # Configs have their own locks and are safe
                            with lock:
                                profiles[name] = s
                if profiles:
                    logger.info(
                        f"Loaded the following profiles (and state):\n[{', '.join(profiles)}]"
                    )
                else:
                    logger.info(f"No profiles found.")

                # Monitor files for changes
                for fd in cfg_fds:
                    try:
                        os.close(fd)
                    except Exception:
                        pass
                cfg_fds = []
                cfg_fns = [
                    CONFIG_DIR,
                    join(CONFIG_DIR, "profiles"),
                ]
                for fn in cfg_fns:
                    fd = os.open(expanduser(fn, ctx), os.O_RDONLY)
                    fcntl.fcntl(
                        fd,
                        fcntl.F_NOTIFY,
                        fcntl.DN_CREATE | fcntl.DN_DELETE | fcntl.DN_MODIFY,
                    )
                    cfg_fds.append(fd)
                should_initialize.clear()

                # Initialize http server
                http_cfg = conf["hhd.http"]
                if http_cfg != prev_http_cfg:
                    prev_http_cfg = http_cfg
                    if https:
                        https.shutdown()
                    if http_cfg["enable"]:
                        from .http import start_http_api

                        port = http_cfg["port"].to(int)
                        localhost = http_cfg["localhost"].to(bool)
                        use_token = http_cfg["token"].to(bool)

                        # Generate security token
                        if use_token:
                            import hashlib
                            import random

                            token = hashlib.sha256(
                                str(random.random()).encode()
                            ).hexdigest()
                            with open(token_fn, "w") as f:
                                f.write(token)

                            sleep(MODIFY_DELAY)
                            should_initialize.clear()
                        else:
                            token = None

                        set_log_plugin("rest")
                        https = start_http_api(
                            apply_cond, conf, profiles, emit, localhost, port, token
                        )
                        update_log_plugins()
                        set_log_plugin("main")

                logger.info(f"Initialization Complete!")

            #
            # Plugin loop
            #

            # Validate config
            validate_config(conf, settings)

            for p in reversed(sorted_plugins):
                set_log_plugin(getattr(p, "log") if hasattr(p, "log") else "ukwn")
                p.prepare(conf)
                update_log_plugins()

            for p in sorted_plugins:
                set_log_plugin(getattr(p, "log") if hasattr(p, "log") else "ukwn")
                p.update(conf)
                update_log_plugins()
            set_log_plugin("ukwn")

            #
            # Save loop
            #

            has_new = should_initialize.is_set()
            saved = False
            # Save existing profiles if open
            if save_state_yaml(state_fn, settings, conf):
                fix_perms(state_fn, ctx)
                saved = True
            for name, prof in profiles.items():
                fn = join(profile_dir, name + ".yml")
                if save_profile_yaml(fn, settings, prof):
                    fix_perms(fn, ctx)
                    saved = True

            # Add template config
            if save_profile_yaml(
                join(profile_dir, "_template.yml"),
                settings,
                templates.get("_template", None),
            ):
                fix_perms(join(profile_dir, "_template.yml"), ctx)
                saved = True

            if not has_new and saved:
                # We triggered the interrupt, clear
                sleep(MODIFY_DELAY)
                should_initialize.clear()

            # Wait for events
            with lock:
                # Notify that events were applied
                apply_cond.notify_all()

                if (
                    not should_exit.is_set()
                    and not should_initialize.is_set()
                    and not emit.has_events()
                ):
                    cond.wait(timeout=POLL_DELAY)

        set_log_plugin("main")
        logger.info(f"HHD Daemon received interrupt, stopping plugins and exiting.")
    finally:
        for fd in cfg_fds:
            try:
                os.close(fd)
            except Exception:
                pass
        if https:
            set_log_plugin("main")
            logger.info("Shutting down the REST API.")
            https.shutdown()
        for plugs in plugins.values():
            for p in plugs:
                set_log_plugin("main")
                logger.info(f"Stopping plugin `{p.name}`.")
                set_log_plugin(getattr(p, "log") if hasattr(p, "log") else "ukwn")
                p.close()


if __name__ == "__main__":
    main()
