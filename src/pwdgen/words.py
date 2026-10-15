"""Access to the bundled BIP39 English wordlist.

The list contains 2048 short words (the BIP39 English standard, MIT licensed)
which makes it ideal for building memorable passphrases.
"""
from __future__ import annotations

from functools import lru_cache

BIP39_WORD_COUNT = 2048


@lru_cache(maxsize=1)
def load_wordlist() -> tuple[str, ...]:
    """Return the bundled wordlist as an immutable tuple of words."""
    from importlib.resources import files

    text = files("pwdgen").joinpath("data").joinpath("words.txt").read_text(
        encoding="utf-8"
    )
    words = tuple(line.strip() for line in text.splitlines() if line.strip())
    if len(words) != BIP39_WORD_COUNT:
        raise RuntimeError(
            f"expected {BIP39_WORD_COUNT} words, found {len(words)}"
        )
    return words
