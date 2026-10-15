"""Tests for :mod:`pwdgen.passphrase` and :mod:`pwdgen.words`."""

import random

import pytest

from pwdgen import passphrase
from pwdgen.words import BIP39_WORD_COUNT, load_wordlist


def test_bundled_wordlist_has_2048_unique_words():
    words = load_wordlist()
    assert len(words) == BIP39_WORD_COUNT
    assert len(set(words)) == BIP39_WORD_COUNT


def test_generate_passphrase_word_count_and_separator():
    phrase = passphrase.generate_passphrase(5, separator=".")
    assert len(phrase.split(".")) == 5


def test_generate_passphrase_is_deterministic_with_seeded_rng():
    words = load_wordlist()
    rng = random.Random(7)
    first = passphrase.generate_passphrase(4, wordlist=words, rng=rng)
    rng = random.Random(7)
    second = passphrase.generate_passphrase(4, wordlist=words, rng=rng)
    assert first == second


def test_generate_passphrase_capitalizes_words():
    words = ("alpha", "bravo", "charlie")
    phrase = passphrase.generate_passphrase(3, capitalize=True, wordlist=words)
    for part in phrase.split("-"):
        assert part[0].isupper()


def test_generate_passphrase_can_include_a_number():
    words = ("alpha", "bravo", "charlie")
    phrase = passphrase.generate_passphrase(
        3, include_number=True, wordlist=words
    )
    parts = phrase.split("-")
    assert len(parts) == 4
    assert any(p.isdigit() for p in parts)


def test_generate_passphrase_rejects_bad_input():
    with pytest.raises(ValueError):
        passphrase.generate_passphrase(0)
    with pytest.raises(ValueError):
        passphrase.generate_passphrase(2, wordlist=[])
