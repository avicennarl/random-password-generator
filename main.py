#!/usr/bin/env python3
"""Backwards-compatible entry point.

This repository used to ship a single ``main.py``. It now delegates to the
``pwdgen`` package so existing instructions keep working:

    python main.py -l 20 -s
    python main.py --passphrase --words 4
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from pwdgen.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
