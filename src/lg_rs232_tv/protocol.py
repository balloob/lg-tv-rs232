"""Protocol helpers for lg_tv_rs232.

LG TV RS232 protocol:

Transmission:
    [Command1][Command2][SPACE][SetID][SPACE][Data][CR]
e.g. "ka 01 ff\\r" to query power.

Response:
    [Command2][SPACE][SetID][SPACE](OK|NG)[Data][x]
e.g. "a 01 OK01x" for "power is on", or "a 01 NGff" on error.

Note that the response is terminated by the literal ASCII character ``x``
(0x78), NOT by a carriage return.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass


class ProtocolError(Exception):
    """Raised when a malformed response is received from the TV."""


class CommandRejected(Exception):
    """Raised when the TV rejects a command with an NG (not-good) acknowledgement.

    LG TVs return NG when a command is not supported by the current model or
    configuration (e.g. volume/mute when audio is routed to optical out), or
    when the data byte is invalid for the command.
    """

    def __init__(self, command2: str, data: str) -> None:
        super().__init__(f"TV rejected command '{command2}' (NG, data={data!r})")
        self.command2 = command2
        self.data = data


_RESPONSE_RE = re.compile(
    r"^(?P<c2>[a-zA-Z])\s+(?P<id>[0-9a-fA-F]{1,2})\s+(?P<status>OK|NG)(?P<data>.*)$"
)


@dataclass(frozen=True)
class Response:
    """Parsed response from the TV."""

    command2: str
    set_id: int
    ok: bool
    data: str

    def raise_for_status(self) -> None:
        if not self.ok:
            raise CommandRejected(self.command2, self.data)


def encode_command(command1: str, command2: str, set_id: int, data: str) -> bytes:
    """Encode a command for transmission to the TV.

    >>> encode_command("k", "a", 1, "ff")
    b'ka 01 ff\\r'
    """
    if len(command1) != 1 or len(command2) != 1:
        raise ValueError("command1 and command2 must each be a single character")
    if not 0 <= set_id <= 99:
        raise ValueError(f"set_id out of range: {set_id}")
    return f"{command1}{command2} {set_id:02d} {data}\r".encode("ascii")


def parse_response(message: str) -> Response:
    """Parse a response message (the body, without the trailing 'x')."""
    match = _RESPONSE_RE.match(message)
    if not match:
        raise ProtocolError(f"Malformed response: {message!r}")
    return Response(
        command2=match.group("c2"),
        set_id=int(match.group("id"), 16),
        ok=match.group("status") == "OK",
        data=match.group("data"),
    )


def percent_to_data(value: int) -> str:
    """Convert a 0..100 integer percent to the 2-char hex data byte.

    >>> percent_to_data(0)
    '00'
    >>> percent_to_data(100)
    '64'
    """
    if not 0 <= value <= 100:
        raise ValueError(f"value out of range 0..100: {value}")
    return f"{value:02x}"


def data_to_percent(data: str) -> int:
    """Convert a 2-char hex data byte (00..64) to a 0..100 integer percent.

    >>> data_to_percent("00")
    0
    >>> data_to_percent("64")
    100
    """
    value = int(data, 16)
    if not 0 <= value <= 100:
        raise ValueError(f"data out of range 0x00..0x64: {data!r}")
    return value


def hex_byte_to_int(data: str) -> int:
    """Parse a 1-2 char hex string to an int."""
    return int(data, 16)


def int_to_hex_byte(value: int) -> str:
    """Format an int (0..255) as a 2-char lowercase hex string."""
    if not 0 <= value <= 0xFF:
        raise ValueError(f"value out of byte range: {value}")
    return f"{value:02x}"


@dataclass
class PendingCommand:
    """A pending command waiting for a response."""

    command2: str
    set_id: int
    future: asyncio.Future[Response]
