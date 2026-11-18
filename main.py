#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261118.

It places the finished front page for 18 November 2026 at
/output/entry.png. Only the standard library is used, nothing is fetched
from the network, and the bytes written are always the same: the program
copies one fixed file, so two runs agree byte for byte.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
from __future__ import annotations

import hashlib
import os
import struct
import sys
from pathlib import Path

SOURCE_NAME = "assets/entry.png"
BYTE_LIMIT = 1_048_576
SIDE_LIMIT = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> "SystemExit":
    """Print an error and stop with a non-zero exit code."""
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def png_dimensions(blob: bytes) -> tuple | None:
    """Return (width, height) from a PNG's IHDR chunk, else None."""
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", blob[16:24])


def run() -> int:
    root = Path(__file__).resolve().parent
    payload = (root / SOURCE_NAME).read_bytes()

    if len(payload) > BYTE_LIMIT:
        raise fail("image is larger than 1 MiB")
    if not payload.startswith(MAGIC):
        raise fail("source image is not a PNG")
    dims = png_dimensions(payload)
    if dims is None or dims[0] > SIDE_LIMIT or dims[1] > SIDE_LIMIT:
        raise fail("image is not a PNG within 1024x1024")

    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "entry.png"
    target.write_bytes(payload)

    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {target} ({len(payload)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
