"""Tests for :mod:`pwdgen.cli`."""

import json

import pytest

from pwdgen.cli import run


def test_cli_prints_one_password_by_default(capsys):
    assert run([]) == 0
    out = capsys.readouterr().out.strip()
    assert len(out) == 16


def test_cli_respects_length_and_count(capsys):
    run(["-l", "24", "-n", "3"])
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 3
    assert all(len(line) == 24 for line in lines)


def test_cli_json_output_contains_strength(capsys):
    run(["--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["type"] == "password"
    assert "entropy_bits" in payload
    assert pub_strength(payload["strength"])


def test_cli_passphrase_mode(capsys):
    run(["--passphrase", "--words", "3"])
    phrase = capsys.readouterr().out.strip()
    assert len(phrase.split("-")) == 3


def test_cli_rejects_invalid_charset(capsys):
    with pytest.raises(SystemExit):
        run(["--no-lower", "--no-upper", "--no-digits"])


def pub_strength(label: str) -> bool:
    return label in {"very weak", "weak", "reasonable", "strong", "very strong"}
