"""
Image organizer class
"""

from typing import Dict
import os
from pathlib import Path

from db.engine import DBInstance
from db.schema import Types
from hashing import file_hasher, dir_hasher

GALLERY_IDENTIFIER = ".gallery"
IMAGE_EXTS = (".jpg", ".jpeg", ".png")
GIF_EXTS = ".gif"
VIDEO_EXTS = ".mp4"


class Organizer:
    """Image organizer class"""

    def __init__(self, root_path: str, db_path: str):
        self._root_path = root_path
        self._db_inst = DBInstance(db_path)
        self._hash_to_file_path: Dict[str, Path] = {}

    def analyze_root(self):
        """Analyze all the files in root path and add them to db if needed"""
        for base, _, files in os.walk(self._root_path):
            if GALLERY_IDENTIFIER in files:
                self._add_directory(base)
            else:
                for file_ in files:
                    self._add_file(base, file_)

    def _add_directory(self, directory):
        dir_path = Path(directory)
        hash_ = dir_hasher.dir_hash(dir_path.resolve())
        type_ = Types.Gallery
        self._db_inst.add_enitity(hash_, type_, dir_path.name)
        self._hash_to_file_path[hash_] = dir_path

    def _add_file(self, base, file_):
        file_path = Path(base, file_)
        hash_ = file_hasher.file_hash(file_path.resolve())
        type_ = self._get_file_type(file_path)
        if not type_:
            return
        self._db_inst.add_enitity(hash_, type_, file_)
        self._hash_to_file_path[hash_] = file_path

    @staticmethod
    def _get_file_type(file_path):
        ext = file_path.suffix.lower()
        if ext in IMAGE_EXTS:
            return Types.Image
        elif ext in GIF_EXTS:
            return Types.Gif
        elif ext in VIDEO_EXTS:
            return Types.Video
        else:
            return None

    def get_entities(self):
        """Get all entities"""
        return self._db_inst.get_enitities()

    def get_types(self):
        """Get all types"""
        return self._db_inst.get_types()

    def get_groupings(self):
        """Get all groupings"""
        return self._db_inst.get_groupings()

    def get_groups(self):
        """Get all groups"""
        return self._db_inst.get_groups()

    def get_file_name(self, hash_):
        """Get file name for given hash"""
        return self._hash_to_file_path.get(hash_)
