#!/usr/bin/env python3
"""Entry program for news-image-20261126.

Copies the pre-drawn front page (entry.png, drawn in code by draw.py)
to the output directory, then verifies the copy is byte-identical to
the source. Standard library only: no Pillow, no network, no side
effects beyond writing entry.png.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry.png missing from repository", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dst)
    if sha256(SOURCE) != sha256(dst):
        print("error: copied entry.png differs from source", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
