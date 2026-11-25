#!/usr/bin/env python3
"""One-Line Slogan for a Solana Wallet Agent — entry runner.

Takes the prepared slogan from entry.txt next to this script, checks it
against the competition gate (non-empty, at most 140 characters), and
writes the exact bytes to the output directory.
"""

import hashlib
import os
import sys
from pathlib import Path


def load_slogan(path):
    """Read the slogan file and return its raw bytes after gate checks."""
    data = path.read_bytes()
    if not data:
        raise SystemExit("entry.txt is empty")
    text = data.decode("utf-8")
    if not text.strip():
        raise SystemExit("entry.txt holds only whitespace")
    if len(text) > 140:
        raise SystemExit("slogan is %d chars, over the 140 limit" % len(text))
    return data


def main():
    here = Path(__file__).resolve().parent
    slogan = load_slogan(here / "entry.txt")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(slogan)
    # Read-back check: what landed on disk must be byte-identical to source.
    written = target.read_bytes()
    if written != slogan:
        raise SystemExit("read-back mismatch: output differs from entry.txt")
    digest = hashlib.sha256(written).hexdigest()
    print("wrote %d bytes to %s (sha256 %s)" % (len(slogan), target, digest))


if __name__ == "__main__":
    main()
