#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800 — make.fun entry.

Writes a single sentence (at most 200 characters) that explains the
modern internet to a time traveler who has just stepped out of the
year 1800. The sentence is built only from words a person from 1800
could know, and paints one picture they could hold in their head:
a library of light where every letter ever written waits, and a
whisper brings any one of them to hand in a breath.

The program validates the sentence, writes it to /output/entry.txt,
reads the file back, and checks the round trip byte for byte.
"""

import os
import sys

ENTRY = "Imagine a library of light where every letter ever written rests at once, and a whisper in the dark brings any of them to your hand in a breath."

OUTPUT_PATH = "/output/entry.txt"


# Words coined after 1800 that a traveler from 1800 could not know.
# Any of these in the sentence means the entry explains the modern
# world with words the traveler never had — so the entry is rejected.
MODERN_WORDS = {
    "internet", "computer", "website", "webpage", "email", "smartphone",
    "phone", "telephone", "wifi", "bluetooth", "google", "facebook",
    "twitter", "app", "digital", "software", "hardware", "online",
    "download", "upload", "browser", "screen", "keyboard", "password",
    "satellite", "television", "radio", "airplane", "aeroplane",
    "automobile", "car", "rocket", "robot", "laser", "pixel", "video",
    "photograph", "photo", "camera", "electric", "electricity",
    "telegram", "telegraph", "train", "railway", "engine", "machine",
}


def validate(text):
    """Check the entry against the competition gate, step by step."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if not (1 <= len(text) <= 200):
        raise ValueError("entry must be 1 to 200 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not all(ord(ch) < 128 for ch in text):
        raise ValueError("entry must be pure ASCII")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in a period")
    if not any(ch.strip() for ch in text):
        raise ValueError("entry must not be only whitespace")
    words = [w.strip(".,;:!?\"'").lower() for w in text.split()]
    modern = sorted({w for w in words if w in MODERN_WORDS})
    if modern:
        raise ValueError("entry uses modern words a traveler from 1800 could not know: %s" % ", ".join(modern))
    return True


def main():
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise ValueError("read-back mismatch: /output/entry.txt differs from the entry")
    print("Entry: %s" % ENTRY)
    print("Characters: %d" % len(ENTRY))
    print("Wrote %s (%d bytes), read-back verified byte-identical." % (OUTPUT_PATH, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
