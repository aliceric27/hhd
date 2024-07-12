def buf(x):
    return bytes(x) + bytes(64 - len(x))


FEATURE_KBD_REPORT_ID = 0x5A

xpad_mode_game = 0x01
xpad_mode_wasd = 0x02
xpad_mode_mouse = 0x03

xpad_cmd_set_mode = 0x01
xpad_cmd_set_mapping = 0x02
xpad_cmd_set_js_dz = 0x04
xpad_cmd_set_tr_dz = 0x05
xpad_cmd_set_vibe_intensity = 0x06
xpad_cmd_check_ready = 0x0A
xpad_cmd_set_calibration = 0x0D
xpad_cmd_set_turbo = 0x0F
xpad_cmd_set_response_curve = 0x13
xpad_cmd_set_adz = 0x18

xpad_axis_xy_left = 0x01
xpad_axis_xy_right = 0x02
xpad_axis_z_left = 0x03
xpad_axis_z_right = 0x04

btn_pair_dpad_u_d = 0x01
btn_pair_dpad_l_r = 0x02
btn_pair_ls_rs = 0x03
btn_pair_lb_rb = 0x04
btn_pair_a_b = 0x05
btn_pair_x_y = 0x06
btn_pair_view_menu = 0x07
btn_pair_m1_m2 = 0x08
btn_pair_lt_rt = 0x09

btn_pair_side_left = 0x00
btn_pair_side_right = 0x01

PAD_A = 0x01
PAD_B = 0x02
PAD_X = 0x03
PAD_Y = 0x04

PAD_LB = 0x05
PAD_RB = 0x06

PAD_LS = 0x07
PAD_RS = 0x08

PAD_DPAD_UP = 0x09
PAD_DPAD_DOWN = 0x0A
PAD_DPAD_LEFT = 0x0B
PAD_DPAD_RIGHT = 0x0C

PAD_VIEW = 0x11
PAD_MENU = 0x12
PAD_XBOX = 0x13


MODE_GAME = buf([FEATURE_KBD_REPORT_ID, 0xD1, xpad_cmd_set_mode, 0x01, xpad_mode_game])

MODE_MOUSE = buf(
    [FEATURE_KBD_REPORT_ID, 0xD1, xpad_cmd_set_mode, 0x01, xpad_mode_mouse]
)

REMAP_DPAD_UD = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_dpad_u_d,
        0x2C,  # Length, 44
        #
        # Each btn_block is 11 bytes.
        #
        # Four btn_blocks:
        # Button 1
        # Button 1 Secondary
        # Button 2
        # Button 2 Secondary
        #
        # Key Groups
        # 1 = Gamepad
        # 2 = Keyboard
        # 3 = Mouse
        # 4 = Key combo, Keyboard
        # 5 = Media
        #
        # btn_block start
        0x01,  # Key Group
        PAD_DPAD_UP,  # Xbox Keycode
        0x00,  # Keyboard Keycode
        0x00,  # Media Keycode
        0x00,  # Mouse Keycode
        0x00,  # Combo length
        0x00,  # Combo Keycode
        0x00,  # Combo Keycode
        0x00,  # Combo Keycode
        0x00,  # Combo Keycode
        0x00,  # Combo Keycode
        #
        # btn_block start
        0x05,
        0x00,
        0x00,
        0x19,  # MEDIA_SHOW_KEYBOARD
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_DPAD_DOWN,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x03,  # Length
        0x8C,  # KB_LCTL
        0x88,  # KB_LSHIFT
        0x76,  # KB_ESC
        0x00,
        0x00,
    ]
)

REMAP_DPAD_UD_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_dpad_u_d,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x98,  # KB_DOWN_ARROW
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x05,
        0x00,
        0x00,
        0x19,  # MEDIA_SHOW_KEYBOARD
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x99,  # KB_UP_ARROW
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x03,  # Length
        0x8C,  # KB_LCTL
        0x88,  # KB_LSHIFT
        0x76,  # KB_ESC
        0x00,
        0x00,
    ]
)

REMAP_DPAD_LR = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_dpad_l_r,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        PAD_DPAD_LEFT,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x23,  # KB_D
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_DPAD_RIGHT,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x0D,  # KB_TAB
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_DPAD_LR_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_dpad_l_r,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x9A,  # KB_LEFT_ARROW
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x23,  # KB_D
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x9B,  # KB_RIGHT_ARROW
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x0D,  # KB_TAB
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_JOYSTICKS = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_ls_rs,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        PAD_LS,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_RS,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_JOYSTICKS_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_ls_rs,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x88,  # KB_LSHIFT
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x03,
        0x00,
        0x00,
        0x00,
        0x01,  # RAT_LCLICK
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_SHOULDERS = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_lb_rb,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        PAD_LB,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_RB,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_SHOULDERS_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_lb_rb,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x0D,  # KB_TAB
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x03,
        0x00,
        0x00,
        0x00,
        0x01,  # RAT_LCLICK
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_AB = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_a_b,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        PAD_A,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x05,
        0x00,
        0x00,
        0x16,  # MEDIA_SCREENSHOT
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_B,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x31,  # KB_N
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_AB_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_a_b,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x5A,  # KB_RET
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x05,
        0x00,
        0x00,
        0x16,  # MEDIA_SCREENSHOT
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x76,  # KB_ESC
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x31,  # KB_N
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_XY = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_x_y,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        PAD_X,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x4D,  # KB_P
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_Y,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x05,
        0x00,
        0x00,
        0x1E,  # MEDIA_START_RECORDING
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_XY_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_x_y,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x97,  # KB_PGDWN
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,  # Length
        0x82,  # KB_META
        0x4D,  # KB_P
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x96,  # KB_PGUP
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x05,
        0x00,
        0x00,
        0x1E,  # MEDIA_START_RECORDING
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_VIEW_MENU = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_view_menu,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        PAD_VIEW,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        PAD_MENU,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_M1M2_DEFAULT = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_m1_m2,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x8E,  # KB_M2
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x8E,  # KB_M2
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x8F,  # KB_M1
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x8F,  # KB_M1
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_M1M2_F17F18 = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_m1_m2,
        0x2C,  # Length, 44
        # btn_block start
        0x02,
        0x00,
        0x28,  # F17?
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x02,
        0x00,
        0x30,  # F18?
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_TRIGGERS = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_lt_rt,
        0x2C,  # Length, 44
        # btn_block start
        0x01,
        0x0D,  # LT
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x01,
        0x0E,  # RT
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

REMAP_TRIGGERS_MOUSE = buf(
    [
        FEATURE_KBD_REPORT_ID,
        0xD1,
        xpad_cmd_set_mapping,
        btn_pair_lt_rt,
        0x2C,  # Length, 44
        # btn_block start
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x02,
        0x88,  # KB_LSHIFT
        0x0D,  # KB_TAB
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x03,
        0x00,
        0x00,
        0x00,
        0x02,  # RAT_RCLICK
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        # btn_block start
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

FLUSH_BUFFER = buf([FEATURE_KBD_REPORT_ID, 0xD1, xpad_cmd_check_ready, 0x01])

COMMIT_RESET = [
    buf(
        [
            FEATURE_KBD_REPORT_ID,
            0xD1,
            xpad_cmd_set_turbo,
            0x20,  # Length, 32
            # Turbo buttons go here.
            # Unknown how they are laid out.
        ]
    ),
    buf(
        [
            FEATURE_KBD_REPORT_ID,
            0xD1,
            xpad_cmd_set_vibe_intensity,
            0x02,  # Length
            0x64,  # Left Intensity
            0x64,  # Right Intensity
        ]
    ),
    buf(
        [
            FEATURE_KBD_REPORT_ID,
            0xD1,
            xpad_cmd_set_js_dz,
            0x04,  # Length
            0x00,  # Left Inner
            0x40,  # Left Outer
            0x00,  # Right Inner
            0x40,  # Right Outer
        ]
    ),
    buf(
        [
            FEATURE_KBD_REPORT_ID,
            0xD1,
            xpad_cmd_set_tr_dz,
            0x04,  # Length
            0x00,  # Left Inner
            0x40,  # Left Outer
            0x00,  # Right Inner
            0x40,  # Right Outer
        ]
    ),
]

COMMANDS_GAME = [
    MODE_GAME,
    FLUSH_BUFFER,
    REMAP_DPAD_LR,
    FLUSH_BUFFER,
    REMAP_DPAD_UD,
    FLUSH_BUFFER,
    REMAP_JOYSTICKS,
    FLUSH_BUFFER,
    REMAP_SHOULDERS,
    FLUSH_BUFFER,
    REMAP_AB,
    FLUSH_BUFFER,
    REMAP_XY,
    FLUSH_BUFFER,
    REMAP_VIEW_MENU,
    FLUSH_BUFFER,
    REMAP_M1M2_F17F18,
    FLUSH_BUFFER,
    REMAP_TRIGGERS,
    *COMMIT_RESET,
]

COMMANDS_MOUSE = [
    MODE_MOUSE,
    FLUSH_BUFFER,
    REMAP_DPAD_UD_MOUSE,
    FLUSH_BUFFER,
    REMAP_DPAD_LR_MOUSE,
    FLUSH_BUFFER,
    REMAP_JOYSTICKS_MOUSE,
    FLUSH_BUFFER,
    REMAP_SHOULDERS_MOUSE,
    FLUSH_BUFFER,
    REMAP_AB_MOUSE,
    FLUSH_BUFFER,
    REMAP_XY_MOUSE,
    FLUSH_BUFFER,
    REMAP_VIEW_MENU,
    FLUSH_BUFFER,
    REMAP_M1M2_F17F18,
    FLUSH_BUFFER,
    REMAP_TRIGGERS_MOUSE,
    *COMMIT_RESET,
]

RGB_APPLY = buf([FEATURE_KBD_REPORT_ID, 0xB4])
RGB_SET = buf([FEATURE_KBD_REPORT_ID, 0xB5])

RGB_INIT_1 = buf([0x5D, 0xB9])
RGB_INIT_2 = buf(
    [
        0x5D,
        0x41,
        0x53,
        0x55,
        0x53,
        0x20,
        0x54,
        0x65,
        0x63,
        0x68,
        0x2E,
        0x49,
        0x6E,
        0x63,
        0x2E,
    ]
)
