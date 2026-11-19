#!/usr/bin/env python3
"""news-image-20261119 entry (nurz v2, globe edition): copy the pre-rendered
image to the output directory. Standard library only; the image is
deterministic because it is produced by compose.py and copied byte-for-byte.
"""

import os
import shutil
import struct
import sys


def _check_png(path):
    """Fail loudly if the entry is not a PNG within the competition limits."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit("entry.png exceeds 1024x1024")
    if os.path.getsize(path) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    _check_png(src)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
