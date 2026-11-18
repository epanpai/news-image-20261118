#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261118.

Writes the 18 November 2026 world-news front page to /output/entry.png.
Standard library only, no network, fully deterministic: the same input
bytes are copied on every run, so both runs write identical bytes.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import struct
import sys

IMAGE = "assets/entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def png_size(data):
    """Read width/height from the PNG IHDR chunk (bytes 16..24)."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(PNG_MAGIC):
        print("error: source image is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("error: image exceeds 1 MiB", file=sys.stderr)
        return 1
    size = png_size(data)
    if size is None or size[0] > MAX_SIDE or size[1] > MAX_SIDE:
        print("error: image is not a valid PNG within 1024x1024",
              file=sys.stderr)
        return 1
    with open(dst, "wb") as f:
        f.write(data)

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
