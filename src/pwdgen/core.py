"""Core building blocks for generating passwords and estimating strength.

The module is deliberately dependency free. Randomness comes from
:mod:`secrets` (a cryptographically secure source) and can be replaced by
passing a ``random.Random``-compatible object, which is what the unit tests
do to obtain deterministic results.
"""
from __future__ import annotations

import math
import secrets

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"

# Characters that are easy to confuse in many fonts.
AMBIGUOUS = "Il1O0o"

__all__ = [
    "LOWERCASE",
    "UPPERCASE",
    "DIGITS",
    "SYMBOLS",
    "AMBIGUOUS",
    "build_charset",
    "generate_password",
    "estimate_entropy",
    "strength_label",
]


def build_charset(
    *,
    lower: bool = True,
    upper: bool = True,
    digits: bool = True,
    symbols: bool = False,
    exclude_ambiguous: bool = False,
) -> str:
    """Return the pool of characters matching the requested options.

    At least one character class must be enabled, otherwise a
    :class:`ValueError` is raised.
    """
    pool = ""
    if lower:
        pool += LOWERCASE
    if upper:
        pool += UPPERCASE
    if digits:
        pool += DIGITS
    if symbols:
        pool += SYMBOLS
    if not pool:
        raise ValueError("at least one character class must be enabled")
    if exclude_ambiguous:
        pool = "".join(ch for ch in pool if ch not in AMBIGUOUS)
        if not pool:
            raise ValueError("charset is empty after removing ambiguous characters")
    return pool


def generate_password(length: int, charset: str, rng=None) -> str:
    """Generate a password of ``length`` characters drawn from ``charset``.

    ``rng`` may be any object exposing a ``choice(seq)`` method; when omitted
    the cryptographically secure :func:`secrets.choice` is used.
    """
    if length < 1:
        raise ValueError("length must be at least 1")
    if not charset:
        raise ValueError("charset must not be empty")
    chooser = rng.choice if rng is not None else secrets.choice
    return "".join(chooser(charset) for _ in range(length))


def estimate_entropy(length: int, pool_size: int) -> float:
    """Estimate the entropy in bits of a uniformly random password."""
    if length < 1 or pool_size < 1:
        return 0.0
    return length * math.log2(pool_size)


def strength_label(bits: float) -> str:
    """Map an entropy value in bits to a human readable strength label."""
    if bits < 28:
        return "very weak"
    if bits < 36:
        return "weak"
    if bits < 60:
        return "reasonable"
    if bits < 128:
        return "strong"
    return "very strong"
