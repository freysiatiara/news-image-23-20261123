#!/usr/bin/env python3
"""news-image-20261123 entry: copy the front-page image to /output/entry.png.

The image (entry.png, 1024x1024, drawn fresh by draw.py in this session)
sums up the world's news of Monday 23 November 2026: COP31 collapses in
Antalya, tanker attacks peak in the Strait of Hormuz, 186 drones over
Ukraine, BepiColombo reaches Mercury, and 32 more stories in 7 regions.
Standard library only; no network. Runs twice, writes identical bytes.
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
DST = os.path.join(OUT_DIR, "entry.png")

MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png too big: {len(data)} bytes", file=sys.stderr)
        return 1
    # Self-check the PNG dimensions straight from the IHDR chunk: the gate
    # allows at most 1024x1024, and both runs must write the same bytes.
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"entry.png too large: {width}x{height}", file=sys.stderr)
        return 1
    print(f"entry.png OK: {width}x{height}, {len(data)} bytes")
    with open(DST, "wb") as f:
        f.write(data)
    print(f"wrote {DST} ({len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
