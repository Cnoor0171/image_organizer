"""Read content of directory and return hash"""

from pathlib import Path
import os
import hashlib

from hashing.file_hasher import file_hash_helper

BUF_SIZE = 64 * 2 ** 10  # 64 kb


def dir_hash(dir_name: Path):
    """Read content of directory and return hash"""

    sha1 = hashlib.sha1()
    for root, _, files in os.walk(dir_name):
        for file_ in files:
            with Path(root, file_).open("rb") as f:
                file_hash_helper(f, sha1)
    return sha1.hexdigest()
