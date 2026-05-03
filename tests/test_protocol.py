"""Tests for the protocol helpers."""

from __future__ import annotations

import pytest

from lg_tv_rs232 import (
    CommandError,
    ProtocolError,
    Response,
    data_to_percent,
    encode_command,
    int_to_hex_byte,
    parse_response,
    percent_to_data,
)


def test_encode_command() -> None:
    assert encode_command("k", "a", 1, "ff") == b"ka 01 ff\r"
    assert encode_command("x", "b", 2, "90") == b"xb 02 90\r"


def test_encode_command_invalid() -> None:
    with pytest.raises(ValueError):
        encode_command("kk", "a", 1, "ff")
    with pytest.raises(ValueError):
        encode_command("k", "a", 100, "ff")


def test_parse_response_ok() -> None:
    resp = parse_response("a 01 OK01")
    assert resp == Response(command2="a", set_id=1, ok=True, data="01")


def test_parse_response_ng() -> None:
    resp = parse_response("f 01 NGff")
    assert not resp.ok
    with pytest.raises(CommandError):
        resp.raise_for_status()


def test_parse_response_invalid() -> None:
    with pytest.raises(ProtocolError):
        parse_response("garbage")


def test_percent_roundtrip() -> None:
    for p in (0, 25, 50, 75, 100):
        assert data_to_percent(percent_to_data(p)) == p


def test_percent_to_data_examples() -> None:
    assert percent_to_data(0) == "00"
    assert percent_to_data(25) == "19"
    assert percent_to_data(50) == "32"
    assert percent_to_data(100) == "64"


def test_percent_out_of_range() -> None:
    with pytest.raises(ValueError):
        percent_to_data(101)
    with pytest.raises(ValueError):
        percent_to_data(-1)
    with pytest.raises(ValueError):
        data_to_percent("ff")


def test_int_to_hex_byte() -> None:
    assert int_to_hex_byte(0) == "00"
    assert int_to_hex_byte(0xC4) == "c4"
    assert int_to_hex_byte(0xFF) == "ff"
    with pytest.raises(ValueError):
        int_to_hex_byte(256)
