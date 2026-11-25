#!/usr/bin/env python3
"""Entry point for news-image-20261125.

Verifies the bundled entry.png (PNG magic, size and dimensions)
and copies it to the output directory (MAKEFUN_OUTPUT_DIR or
/output). Standard library only, no network.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    """Return (width, height) from a PNG header, or raise ValueError."""
    with open(path, "rb") as fh:
        head = fh.read(33)
        fh.seek(-12, os.SEEK_END)
        tail = fh.read(12)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    if tail[4:8] != b"IEND":
        raise ValueError("PNG is truncated: no IEND chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width <= 0 or height <= 0:
        raise ValueError("invalid PNG dimensions")
    return width, height


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB: %d bytes" % size)
    width, height = read_png_size(SRC)
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit("entry.png too large: %dx%d" % (width, height))

    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    if sha256_of(dest) != sha256_of(SRC):
        sys.exit("copy verification failed: hash mismatch")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dest, width, height, size, sha256_of(dest)[:16]))


if __name__ == "__main__":
    main()
