"""Constants and enums shared across the lg_rs232_tv package."""

from enum import Enum

BAUD_RATE = 9600
COMMAND_TIMEOUT = 2.0  # seconds to wait for a response
INTER_COMMAND_DELAY = 0.05  # seconds to wait between commands
CR = b"\r"
ACK_TERMINATOR = b"x"  # responses end with the literal character 'x'

DEFAULT_SET_ID = 1  # broadcast-ish; LG TVs default to 01

# Volume range (TV percent: 0..100)
MIN_VOLUME = 0
MAX_VOLUME = 100

# Picture-related percent ranges
MIN_PERCENT = 0
MAX_PERCENT = 100


class PowerState(Enum):
    """Receiver chassis power state."""

    OFF = "OFF"
    ON = "ON"


class InputSource(Enum):
    """TV input sources (xb command, modern format).

    Values are the hex bytes sent over the wire (lowercase).
    """

    DTV_ANTENNA = "00"
    DTV_CABLE = "01"
    ANALOG_ANTENNA = "10"
    ANALOG_CABLE = "11"
    AV1 = "20"
    AV2 = "21"
    COMPONENT1 = "40"
    COMPONENT2 = "41"
    COMPONENT3 = "42"
    RGB_PC = "60"
    HDMI1 = "90"
    HDMI2 = "91"
    HDMI3 = "92"
    HDMI4 = "93"


class LegacyInputSource(Enum):
    """Legacy input sources (kb command, pre-2010 sets)."""

    DTV = "00"
    ANALOG = "01"
    VIDEO1 = "02"
    VIDEO2 = "03"
    COMPONENT1 = "04"
    COMPONENT2 = "05"
    RGB_DTV = "06"
    RGB_PC = "07"
    DVI_DTV = "08"  # also HDMI1/DVI on some sets
    DVI_PC = "09"  # also HDMI2 on some sets


class AspectRatio(Enum):
    """Aspect ratio (kc)."""

    R_4_3 = "01"
    R_16_9 = "02"
    HORIZON = "03"
    ZOOM_1 = "04"
    ZOOM_2 = "05"
    SET_BY_PROGRAM = "06"
    R_14_9 = "07"
    FULL = "08"
    JUST_SCAN = "09"
    ZOOM_3 = "0a"
    FULL_WIDE = "0b"
    CINEMA_ZOOM_1 = "10"
    CINEMA_ZOOM_16 = "1f"


class ScreenMute(Enum):
    """Screen / video-out mute (kd)."""

    OFF = "00"
    SCREEN_ON = "01"  # picture off
    VIDEO_OUT_ON = "10"


class ColorTemperature(Enum):
    """Color temperature presets (ku / xu)."""

    MEDIUM = "00"
    COOL = "01"
    WARM = "02"
    USER = "03"
    NATURAL = "04"


class ISMMethod(Enum):
    """ISM method - plasma image-retention prevention (jp)."""

    ORBITER = "02"
    WHITE_WASH = "04"
    NORMAL = "08"
    COLOR_WASH = "20"


class EnergySaving(Enum):
    """Energy / power saving levels (jq)."""

    OFF = "00"
    MINIMUM = "01"
    MEDIUM = "02"
    MAXIMUM = "03"
    AUTO = "04"
    SCREEN_OFF = "05"


class PictureMode(Enum):
    """Picture mode preset (dx)."""

    VIVID = "00"
    STANDARD = "01"
    CINEMA = "02"
    SPORT = "03"
    GAME = "04"
    EXPERT_1 = "05"
    EXPERT_2 = "06"
    APS = "08"  # power-saving picture mode


class SoundMode(Enum):
    """Sound mode preset (dy)."""

    STANDARD = "01"
    MUSIC = "02"
    CINEMA = "03"
    SPORT = "04"
    GAME = "05"


class TileMode(Enum):
    """Tile / video-wall mode (dd) - common values."""

    OFF = "00"
    ON = "01"


class ThreeDMode(Enum):
    """3D mode (xt) - data1 values."""

    ON = "00"
    OFF = "01"
    THREE_D_TO_TWO_D = "02"
    TWO_D_TO_THREE_D = "03"


class PIPMode(Enum):
    """PIP / DW / POP mode (kn)."""

    OFF = "00"
    PIP = "01"
    DW1 = "02"
    DW2 = "03"
    DW3 = "04"
    POP4 = "05"
    POP9 = "06"
    POP13 = "07"


class PIPPosition(Enum):
    """PIP position (kq)."""

    RIGHT_DOWN = "00"
    LEFT_DOWN = "01"
    LEFT_UP = "02"
    RIGHT_UP = "03"


class RemoteKey(Enum):
    """Remote control key codes (mc).

    The TV accepts the same hex codes that the IR remote emits, sent as the
    data byte of the `mc` command. Only a subset of common keys is enumerated;
    use ``LGTV.send_remote_key_code(0x..)`` for arbitrary codes.
    """

    # Power
    POWER = "08"
    POWER_ON = "c4"
    POWER_OFF = "c5"

    # Channel / volume
    CHANNEL_UP = "00"
    CHANNEL_DOWN = "01"
    VOLUME_UP = "02"
    VOLUME_DOWN = "03"
    MUTE = "09"

    # Navigation
    UP = "40"
    DOWN = "41"
    LEFT = "07"
    RIGHT = "06"
    OK = "44"
    HOME = "7c"
    MENU = "43"
    BACK = "28"
    EXIT = "5b"
    INFO = "aa"

    # Number keys
    NUM_0 = "10"
    NUM_1 = "11"
    NUM_2 = "12"
    NUM_3 = "13"
    NUM_4 = "14"
    NUM_5 = "15"
    NUM_6 = "16"
    NUM_7 = "17"
    NUM_8 = "18"
    NUM_9 = "19"

    # Aspect ratio
    RATIO_4_3 = "76"
    RATIO_16_9 = "77"
    RATIO_ZOOM = "af"

    # Inputs (single-button shortcuts)
    INPUT_TV = "0f"
    INPUT_TV_AV = "0b"
    INPUT_HDMI1 = "ce"
    INPUT_HDMI2 = "cc"
    INPUT_HDMI3 = "e9"
    INPUT_HDMI4 = "da"
    INPUT_COMPONENT1 = "bf"
    INPUT_COMPONENT2 = "d4"
    INPUT_COMPONENT3 = "d9"
    INPUT_AV1 = "5a"
    INPUT_AV2 = "d0"
    INPUT_RGB_PC = "d5"

    # Media
    PLAY = "b0"
    PAUSE = "ba"
    STOP = "b1"
    REWIND = "8f"
    FAST_FORWARD = "8e"

    # Misc
    SUBTITLE = "39"  # closed captions
    Q_MENU = "45"
    SIMPLINK = "7e"
    LIST = "4c"
    GUIDE = "ab"
    FAV = "1e"
    THREE_D = "dc"
