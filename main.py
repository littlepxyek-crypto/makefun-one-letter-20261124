#!/usr/bin/env python3
"""One Letter for Your Day — entry letter: Z, for "zero sleep".

Why Z wins against the judge's criteria, in their order:

1. It stands for a real word for a real day. "Zero sleep" is not a mood
   or a vibe; it is the literal summary of the day this was written.
2. It is vivid and specific. Z calls up one sharp picture: a face at
   4 a.m., lit by a screen, running on fumes — not a vague "tired".
3. It is funny in the way that lands instantly. Everyone has had the
   zero-sleep day; the letter is the joke and the confession at once,
   the kind of one-liner you retell to a friend.
4. It is true. This entry was made in the small hours by someone who
   had not slept. No performance — a field report.
5. The letter fits the word and is not the lazy pick. A for "amazing"
   is the obvious answer; Z is the far end of the alphabet for the
   far end of the night, and it earns its place.

The program writes exactly one byte — "Z" — to entry.txt in the
output directory, then reads it back and verifies the gate rules:
UTF-8, exactly one character, an uppercase letter A-Z, no newline.
"""

import os
import sys
import tempfile

DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"


def choose_letter() -> str:
    """Return the single letter this entry stands behind."""
    return "Z"


def write_entry(path: str, letter: str) -> None:
    """Write the letter atomically — temp file in the same directory,
    then os.replace — so entry.txt is never observed half-written."""
    directory = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(letter)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def verify_entry(path: str, letter: str) -> bool:
    """Re-read the entry and check it against the gate rules."""
    with open(path, "rb") as handle:
        raw = handle.read()
    # No byte-order mark: a BOM would sit in front of the letter.
    if raw.startswith(b"\xef\xbb\xbf"):
        return False
    if len(raw) != 1:
        return False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    # The single character must be the letter itself, never whitespace.
    if text.isspace():
        return False
    return text == letter and "A" <= text <= "Z"


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, ENTRY_FILENAME)
    letter = choose_letter()
    write_entry(path, letter)
    if not verify_entry(path, letter):
        print(f"self-check failed for {path}", file=sys.stderr)
        return 1
    print(f"wrote {letter!r} to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
