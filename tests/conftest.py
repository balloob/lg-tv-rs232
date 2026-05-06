"""Shared test fixtures for lg_rs232_tv."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import lg_rs232_tv
import lg_rs232_tv.tv as lg_tv_module
from lg_rs232_tv import LGTV

# Speed up tests
lg_rs232_tv.COMMAND_TIMEOUT = 0.1
lg_tv_module.COMMAND_TIMEOUT = 0.1


# Each entry maps "command-as-sent" (e.g. "ka 01 ff") to the response data
# string the mock TV should reply with (e.g. "01" -> "a 01 OK01x"). NG
# responses can be triggered by prefixing with "NG:" (e.g. "NG:ff").
DEFAULT_RESPONSES: dict[str, str] = {
    "ka 01 ff": "01",        # power on
    "xb 01 ff": "90",        # input HDMI1
    "kc 01 ff": "02",        # aspect 16:9
    "kd 01 ff": "00",        # screen mute off
    "ke 01 ff": "01",        # mute off
    "kf 01 ff": "1e",        # volume 30
    "kg 01 ff": "32",        # contrast 50
    "kh 01 ff": "32",        # brightness 50
    "ki 01 ff": "32",        # color 50
    "kj 01 ff": "32",        # tint 50
    "kk 01 ff": "32",        # sharpness 50
    "kl 01 ff": "01",        # osd on
    "km 01 ff": "00",        # remote lock off
    "kr 01 ff": "32",        # treble 50
    "ks 01 ff": "32",        # bass 50
    "kt 01 ff": "32",        # balance 50
    "ku 01 ff": "00",        # color temp medium
    "jq 01 ff": "00",        # energy saving off
    "mg 01 ff": "50",        # backlight 80
    "dx 01 ff": "01",        # picture mode standard
    "dy 01 ff": "01",        # sound mode standard
}


class MockSerialConnection:
    """Mock serial reader/writer pair with auto-response support."""

    def __init__(self) -> None:
        self.reader = asyncio.StreamReader()
        self.writer = MagicMock()
        self.writer.write = MagicMock()
        self.writer.drain = AsyncMock()
        self.writer.close = MagicMock()
        self.writer.wait_closed = AsyncMock()
        self.written: list[bytes] = []
        self.responses: dict[str, str] = {}
        self.command_handler: Callable[[str], None] | None = None
        self.writer.write.side_effect = self._on_write

    def _on_write(self, data: bytes) -> None:
        self.written.append(data)
        cmd = data.decode("ascii").rstrip("\r")
        # cmd looks like "ka 01 ff" or "kf 01 32"
        parts = cmd.split(" ")
        c1c2 = parts[0]
        c2 = c1c2[1]
        set_id = parts[1]

        if cmd in self.responses:
            value = self.responses[cmd]
            if value.startswith("NG:"):
                self.feed(f"{c2} {set_id} NG{value[3:]}x")
            else:
                self.feed(f"{c2} {set_id} OK{value}x")
        elif self.command_handler is not None:
            self.command_handler(cmd)

    def feed(self, message: str) -> None:
        """Inject a raw message (without CR) into the reader."""
        self.reader.feed_data(message.encode("ascii"))


@pytest.fixture
async def mock_serial() -> MockSerialConnection:
    return MockSerialConnection()


@pytest.fixture
async def tv(mock_serial: MockSerialConnection):
    """Create a connected LGTV with mocked serial."""
    tv = LGTV("/dev/ttyUSB0")
    mock_serial.responses = dict(DEFAULT_RESPONSES)

    async def fake_open(*args, **kwargs):
        return mock_serial.reader, mock_serial.writer

    with patch(
        "lg_rs232_tv.tv.serialx.open_serial_connection",
        side_effect=fake_open,
    ):
        await tv.connect()

    yield tv

    if tv.connected:
        await tv.disconnect()
