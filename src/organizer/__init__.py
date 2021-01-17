"""
Image organizer class
"""

from typing import Dict
import os
from pathlib import Path

from organizer.db.db_instance import DBInstance
from organizer.db.schema import EntityTypeId
from organizer.hashing import file_hasher, dir_hasher

GALLERY_IDENTIFIER = ".gallery"
IMAGE_EXTS = (".jpg", ".jpeg", ".png")
GIF_EXTS = (".gif",)
VIDEO_EXTS = (".mp4", ".flv")


class Organizer:
    """Image organizer class"""

    def __init__(self, root_path: str, db_path: str):
        self._root_path = root_path
        self._db_inst = DBInstance(db_path)
        self._hash_to_file_path: Dict[str, Path] = {}

    def analyze_root(self):
        """Analyze all the files in root path and add them to db if needed"""
        for base, sub_dirs, files in os.walk(self._root_path):
            if GALLERY_IDENTIFIER in files:
                self._add_directory(base)
                sub_dirs[:] = []
            else:
                for file_ in files:
                    self._add_file(base, file_)

    def _add_directory(self, directory):
        dir_path = Path(directory)
        hash_ = dir_hasher.dir_hash(dir_path.resolve())
        type_ = EntityTypeId.Gallery
        self._db_inst.add_enitity(hash_, type_, dir_path.name)
        self._hash_to_file_path[hash_] = dir_path

    def _add_file(self, base, file_):
        file_path = Path(base, file_)
        hash_ = file_hasher.file_hash(file_path.resolve())
        type_ = self._get_file_type(file_path)
        self._db_inst.add_enitity(hash_, type_, file_)
        self._hash_to_file_path[hash_] = file_path

    @staticmethod
    def _get_file_type(file_path):
        ext = file_path.suffix.lower()
        if ext in IMAGE_EXTS:
            return EntityTypeId.Image
        elif ext in GIF_EXTS:
            return EntityTypeId.Gif
        elif ext in VIDEO_EXTS:
            return EntityTypeId.Video
        else:
            return EntityTypeId.Unkown

    def get_all_entities(self):
        """Get all entities"""
        return self._db_inst.get_all_entities()

    def get_entity_by_id(self, entity_id: int):
        """Get one entity by id"""
        return self._db_inst.get_entity_by_id(entity_id)

    def get_entity_by_hash(self, entity_hash: str):
        """Get one entity by hash"""
        return self._db_inst.get_entity_by_hash(entity_hash)

    def get_all_entity_types(self):
        """Get all entity types"""
        return self._db_inst.get_all_entity_types()

    def get_entity_type_by_id(self, id_: EntityTypeId):
        """Get one entity type by id"""
        return self._db_inst.get_entity_type_by_id(id_)

    def get_all_groupings(self):
        """Get all groupings"""
        return self._db_inst.get_all_groupings()

    def get_grouping_by_id(self, id_: int):
        """Get one grouping by id"""
        return self._db_inst.get_grouping_by_id(id_)

    def get_all_groups(self):
        """Get all groups"""
        return self._db_inst.get_all_groups()

    def get_group_by_id(self, id_: int):
        """Get one group by id"""
        return self._db_inst.get_group_by_id(id_)

    def get_file_name_by_hash(self, hash_):
        """Get file name for given hash"""
        return self._hash_to_file_path.get(hash_)
