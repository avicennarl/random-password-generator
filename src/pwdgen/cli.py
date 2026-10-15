"""Command line interface for ``pwdgen``."""
from __future__ import annotations

import argparse
import json
import math
import sys

from pwdgen import __version__
from pwdgen.core import (
    build_charset,
    estimate_entropy,
    generate_password,
    strength_label,
)
from pwdgen.passphrase import generate_passphrase

BITS_PER_WORD = math.log2(2048)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pwdgen",
        description=(
            "Generate cryptographically secure passwords and passphrases, "
            "fully offline."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("-n", "--count", type=int, default=1, help="how many to generate")
    parser.add_argument("--json", action="store_true", help="print JSON instead of plain text")

    parser.add_argument("-l", "--length", type=int, default=16, help="password length")
    parser.add_argument("--no-lower", action="store_true", help="exclude lowercase letters")
    parser.add_argument("--no-upper", action="store_true", help="exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="exclude digits")
    parser.add_argument("-s", "--symbols", action="store_true", help="include symbols")
    parser.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="drop easily confused characters (Il1O0o)",
    )

    parser.add_argument("-p", "--passphrase", action="store_true", help="generate a passphrase")
    parser.add_argument("-w", "--words", type=int, default=4, help="words per passphrase")
    parser.add_argument("--separator", default="-", help="passphrase word separator")
    parser.add_argument("--capitalize", action="store_true", help="capitalize each word")
    parser.add_argument(
        "--number", action="store_true", help="insert a random digit into a passphrase"
    )
    return parser


def _passphrase_entropy(n_words: int, include_number: bool) -> float:
    bits = n_words * BITS_PER_WORD
    if include_number:
        bits += math.log2(10) + math.log2(n_words + 1)
    return bits


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.count < 1:
        parser.error("--count must be at least 1")

    results: list[dict[str, object]] = []
    if args.passphrase:
        if args.words < 1:
            parser.error("--words must be at least 1")
        bits = _passphrase_entropy(args.words, args.number)
        for _ in range(args.count):
            value = generate_passphrase(
                args.words,
                separator=args.separator,
                capitalize=args.capitalize,
                include_number=args.number,
            )
            results.append(_record("passphrase", value, bits))
    else:
        try:
            charset = build_charset(
                lower=not args.no_lower,
                upper=not args.no_upper,
                digits=not args.no_digits,
                symbols=args.symbols,
                exclude_ambiguous=args.exclude_ambiguous,
            )
        except ValueError as exc:
            parser.error(str(exc))
        bits = estimate_entropy(args.length, len(charset))
        for _ in range(args.count):
            value = generate_password(args.length, charset)
            results.append(_record("password", value, bits))

    if args.json:
        payload = results if len(results) > 1 else results[0]
        print(json.dumps(payload, indent=2))
    else:
        for record in results:
            print(record["value"])
    return 0


def _record(kind: str, value: str, bits: float) -> dict[str, object]:
    return {
        "type": kind,
        "value": value,
        "entropy_bits": round(bits, 1),
        "strength": strength_label(bits),
    }


def main(argv: list[str] | None = None) -> None:
    try:
        raise SystemExit(run(argv))
    except BrokenPipeError:  # pragma: no cover - happens when piping to head
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
