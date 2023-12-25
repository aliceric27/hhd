import datetime
import logging
import os
import pathlib
from logging.handlers import RotatingFileHandler
from typing import Sequence, Any

from rich.logging import RichHandler

from .utils import Context, expanduser

logger = logging.getLogger(__name__)

RASTER = """\
   _______   _______    ______  
  /    /  ╲╲/    /  ╲╲_/      ╲╲
 /        //        //        //
/         /         /         / 
╲___/____/╲___/____/╲________/  \n"""


class NewLineFormatter(logging.Formatter):
    """Aligns newlines during multiline prints."""

    def format(self, record):
        msg = super().format(record)
        if (idx := msg.index("|||")) != -1:
            preamble = msg[:idx]
            msg = msg.replace("|||", "").replace("\n", "\n" + (" " * len(preamble)))
        return msg


_plugins = []


def set_log_alias(plugins: Sequence[tuple[str, str]]):
    global _plugins
    _plugins = plugins


class PluginLogRender:
    def __init__(
        self,
        time_format="[%x %X]",
        omit_repeated_times: bool = True,
        level_width=8,
        plugin_width=8,
    ) -> None:
        from rich.style import Style

        self.time_format = time_format
        self.omit_repeated_times = omit_repeated_times
        self.level_width = level_width
        self._last_time = None
        self.plugin_width = plugin_width

    def __call__(
        self,
        console,
        renderables,
        log_time=None,
        time_format=None,
        level: Any = "",
        plugin: str | None = None,
        path: str | None = None,
        line_no: int | None = None,
        link_path: str | None = None,
    ):
        from rich.containers import Renderables
        from rich.table import Table
        from rich.text import Text

        output = Table.grid(padding=(0, 1))
        output.expand = True
        output.add_column(style="log.time")
        output.add_column(style="log.level", width=self.level_width)
        output.add_column(
            style="magenta" if plugin == "main" else "cyan", width=self.plugin_width
        )

        output.add_column(ratio=1, style="log.message", overflow="fold")
        output.add_column(style="log.path")

        row = []
        log_time = log_time or console.get_datetime()
        time_format = time_format or self.time_format
        if callable(time_format):
            log_time_display = time_format(log_time)
        else:
            log_time_display = Text(log_time.strftime(time_format))
        if log_time_display == self._last_time and self.omit_repeated_times:
            row.append(Text(" " * len(log_time_display)))
        else:
            row.append(log_time_display)
            self._last_time = log_time_display
        row.append(level)
        row.append(plugin.upper() if plugin else "")

        # Find plugin
        row.append(Renderables(renderables))
        if path:
            path_text = Text()
            path_text.append(
                path, style=f"link file://{link_path}" if link_path else ""
            )
            if line_no:
                path_text.append(":")
                path_text.append(
                    f"{line_no}",
                    style=f"link file://{link_path}#{line_no}" if link_path else "",
                )
            row.append(path_text)

        output.add_row(*row)
        return output


class PluginRichHandler(RichHandler):
    def __init__(self, renderer: PluginLogRender) -> None:
        self.renderer = renderer
        super().__init__()

    def render(
        self,
        *,
        record,
        traceback,
        message_renderable,
    ):
        path = pathlib.Path(record.pathname).name
        level = self.get_level_text(record)
        time_format = None if self.formatter is None else self.formatter.datefmt
        log_time = datetime.datetime.fromtimestamp(record.created)

        plugin = None
        module = record.name
        for p, name in _plugins:
            if module.startswith(p):
                plugin = name
                break

        log_renderable = self.renderer(
            self.console,
            [message_renderable] if not traceback else [message_renderable, traceback],
            log_time=log_time,
            time_format=time_format,
            level=level,
            plugin=plugin,
            path=path,
            line_no=record.lineno,
            link_path=record.pathname if self.enable_link_path else None,
        )
        return log_renderable


class UserRotatingFileHandler(RotatingFileHandler):
    def __init__(
        self,
        filename: str,
        mode: str = "a",
        maxBytes: int = 0,
        backupCount: int = 0,
        encoding: str | None = None,
        delay: bool = False,
        errors: str | None = None,
        ctx: Context | None = None,
    ) -> None:
        self.ctx = ctx
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay, errors)

    def _open(self):
        d = super()._open()
        if self.ctx:
            os.chown(self.baseFilename, self.ctx.euid, self.ctx.egid)
        return d


def setup_logger(
    log_dir: str | None = None, init: bool = True, ctx: Context | None = None
):
    from rich import get_console
    from rich.traceback import install

    if log_dir:
        log_dir = expanduser(log_dir, ctx)

    install()
    handlers = []
    handlers.append(PluginRichHandler(PluginLogRender()))
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        handler = UserRotatingFileHandler(
            os.path.join(log_dir, "hhd.log"),
            maxBytes=10_000_000,
            backupCount=10,
            ctx=ctx,
        )
        handler.setFormatter(
            NewLineFormatter("%(asctime)s %(module)-15s %(levelname)-8s|||%(message)s")
        )
        handler.doRollover()
        handlers.append(handler)

    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.INFO,
        datefmt="[%d/%m %H:%M]",
        format=FORMAT,
        handlers=handlers,
    )
    if init:
        get_console().print(RASTER, justify="full", markup=False, highlight=False)
        logger.info(f"Handheld Daemon starting...")
