"""Read content of file and return hash"""

import hashlib
from typing import BinaryIO
from pathlib import Path

BUF_SIZE = 64 * 2 ** 10  # 64 kb


def file_hash(file_name: Path) -> str:
    """Read content of file and return hash"""
    sha1 = hashlib.sha1()
    with file_name.open("rb") as inf:
        file_hash_helper(inf, sha1)
        return sha1.hexdigest()


def file_hash_helper(f: BinaryIO, sha1):
    """Read content of file object and appends to hash"""
    while True:
        file_content = f.read(BUF_SIZE)
        if not file_content:
            break
        sha1.update(file_content)
