"""Runtime state dataclasses for lg_tv_rs232."""

from __future__ import annotations

from dataclasses import dataclass, replace

from .const import (
    AspectRatio,
    ColorTemperature,
    EnergySaving,
    InputSource,
    PictureMode,
    PowerState,
    ScreenMute,
    SoundMode,
)


@dataclass
class TVState:
    """Snapshot of the LG TV's current state.

    All fields are ``None`` until the corresponding attribute has been
    queried (or pushed via an explicit set).
    """

    power: PowerState | None = None
    input_source: InputSource | None = None
    aspect_ratio: AspectRatio | None = None
    screen_mute: ScreenMute | None = None
    volume_mute: bool | None = None  # True = muted

    # 0..100 percent
    volume: int | None = None
    contrast: int | None = None
    brightness: int | None = None
    color: int | None = None
    tint: int | None = None
    sharpness: int | None = None
    backlight: int | None = None
    treble: int | None = None
    bass: int | None = None
    balance: int | None = None

    color_temperature: ColorTemperature | None = None
    energy_saving: EnergySaving | None = None
    picture_mode: PictureMode | None = None
    sound_mode: SoundMode | None = None

    osd_enabled: bool | None = None
    remote_lock: bool | None = None

    def copy(self) -> TVState:
        return replace(self)
