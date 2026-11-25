#!/usr/bin/env python3
"""Fortune Cookie for the Liquidated Trader.

Writes one fortune-cookie line for a crypto trader who has just been
liquidated, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line keeps the fortune voice: an oracular opening the punchline then
breaks. No network, no randomness, no input, no time dependence: the same
line on every run, so the entry is byte-identical wherever it is graded.
"""

import os
import sys

FORTUNE = (
    "The stars predict great wealth in your future. "
    "They did not say whose wallet it would be in."
)

MAX_CHARS = 160
MAX_WORDS = 20


def check_gate(text):
    """Mirror the house gate: 1-160 chars, one line, non-whitespace UTF-8,
    at most 20 words of plain text."""
    if not isinstance(text, str):
        return "not text"
    if not text.strip():
        return "only white space"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return "length %d outside 1-%d chars" % (len(text), MAX_CHARS)
    if "\n" in text or "\r" in text:
        return "more than one line"
    words = text.split()
    if len(words) > MAX_WORDS:
        return "%d words, over the %d-word cap" % (len(words), MAX_WORDS)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "not UTF-8 text"
    return None


def main():
    problem = check_gate(FORTUNE)
    if problem is not None:
        print("gate FAIL: %s" % problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(FORTUNE)
    with open(path, "rb") as f:
        raw = f.read()
    if raw != FORTUNE.encode("utf-8"):
        print("round-trip FAIL: bytes on disk differ", file=sys.stderr)
        return 1
    problem = check_gate(raw.decode("utf-8"))
    if problem is not None:
        print("gate FAIL on disk content: %s" % problem, file=sys.stderr)
        return 1
    print(FORTUNE)
    print("chars=%d words=%d" % (len(FORTUNE), len(FORTUNE.split())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
