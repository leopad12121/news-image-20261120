#!/usr/bin/env python3
"""Entry point for the news-image-20261120 bounty.

Copies the pre-rendered front page (entry.png, produced by draw_news.py)
into the grader's output directory, verifying the copy byte-for-byte.

Standard library only. The source image is resolved relative to this
script's own directory, never the current working directory, so the
program works no matter where it is launched from.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("error: cannot create output directory: %s" % exc, file=sys.stderr)
        return 1

    dest = Path(out_dir) / "entry.png"
    try:
        shutil.copyfile(source, dest)
    except OSError as exc:
        print("error: cannot copy entry.png: %s" % exc, file=sys.stderr)
        return 1

    try:
        source_hash = sha256_of(source)
        dest_hash = sha256_of(dest)
    except OSError as exc:
        print("error: cannot hash entry.png: %s" % exc, file=sys.stderr)
        return 1

    if source_hash != dest_hash:
        print("error: SHA-256 mismatch after copy", file=sys.stderr)
        return 1

    print("copied entry.png to %s (sha256 %s)" % (dest, dest_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
