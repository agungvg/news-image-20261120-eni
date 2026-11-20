#!/usr/bin/env python3
"""Copy the committed front page to the grader's output directory.

The front page is rendered by draw.py and committed as entry.png; this
entrypoint only copies it to $MAKEFUN_OUTPUT_DIR/entry.png and checks
the copy (PNG signature, same size, identical sha256).

Stdlib only, no network, no clock, no randomness, so it runs on the
grader's read-only mount where the repository itself cannot be written.
"""
import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(src) != os.path.getsize(dst):
        print("error: size changed during copy", file=sys.stderr)
        return 1
    with open(dst, "rb") as f:
        if f.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print("error: copy is not a PNG file", file=sys.stderr)
            return 1
    if sha256_file(src) != sha256_file(dst):
        print("error: hash changed during copy", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
