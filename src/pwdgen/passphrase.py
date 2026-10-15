"""Passphrase generation from a wordlist."""
from __future__ import annotations

import secrets
from collections.abc import Sequence

from pwdgen.words import load_wordlist


def generate_passphrase(
    n_words: int = 4,
    *,
    separator: str = "-",
    capitalize: bool = False,
    include_number: bool = False,
    wordlist: Sequence[str] | None = None,
    rng=None,
) -> str:
    """Build a passphrase from ``n_words`` random words.

    ``rng`` may be any object exposing a ``choice(seq)`` method; when omitted
    the cryptographically secure :func:`secrets.choice` is used.
    """
    if n_words < 1:
        raise ValueError("n_words must be at least 1")
    words = wordlist if wordlist is not None else load_wordlist()
    if not words:
        raise ValueError("wordlist must not be empty")

    chooser = rng.choice if rng is not None else secrets.choice
    chosen = [chooser(words) for _ in range(n_words)]
    if capitalize:
        chosen = [w.capitalize() for w in chosen]
    if include_number:
        number = str(chooser("0123456789"))
        position = chooser(range(len(chosen) + 1))
        chosen.insert(position, number)
    return separator.join(chosen)
