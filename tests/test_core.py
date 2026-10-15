"""Unit tests for :mod:`pwdgen.core`."""

import math
import random

import pytest

from pwdgen import core


def test_build_charset_default_has_lower_upper_digits_only():
    pool = core.build_charset()
    assert set(core.LOWERCASE) <= set(pool)
    assert set(core.UPPERCASE) <= set(pool)
    assert set(core.DIGITS) <= set(pool)
    assert not (set(core.SYMBOLS) & set(pool))


def test_build_charset_symbols_flag_adds_symbols():
    pool = core.build_charset(symbols=True)
    assert set(core.SYMBOLS) <= set(pool)


def test_build_charset_exclude_ambiguous_removes_confusing_characters():
    pool = core.build_charset(exclude_ambiguous=True)
    assert not (set(core.AMBIGUOUS) & set(pool))


def test_build_charset_requires_at_least_one_class():
    with pytest.raises(ValueError):
        core.build_charset(lower=False, upper=False, digits=False)


def test_generate_password_length_and_alphabet():
    pool = core.build_charset()
    password = core.generate_password(24, pool)
    assert len(password) == 24
    assert set(password) <= set(pool)


def test_generate_password_is_deterministic_with_seeded_rng():
    rng = random.Random(42)
    first = core.generate_password(16, core.build_charset(), rng=rng)
    rng = random.Random(42)
    second = core.generate_password(16, core.build_charset(), rng=rng)
    assert first == second


def test_generate_password_rejects_bad_arguments():
    with pytest.raises(ValueError):
        core.generate_password(0, core.build_charset())
    with pytest.raises(ValueError):
        core.generate_password(8, "")


def test_estimate_entropy_matches_formula():
    assert core.estimate_entropy(10, 10) == pytest.approx(10 * math.log2(10))


def test_estimate_entropy_zero_for_empty_inputs():
    assert core.estimate_entropy(0, 10) == 0.0
    assert core.estimate_entropy(10, 0) == 0.0


@pytest.mark.parametrize(
    "bits,expected",
    [
        (10, "very weak"),
        (30, "weak"),
        (40, "reasonable"),
        (80, "strong"),
        (200, "very strong"),
    ],
)
def test_strength_label_thresholds(bits, expected):
    assert core.strength_label(bits) == expected
