"""Db schema definitions for entity type"""
from enum import IntEnum
from dataclasses import dataclass

import sqlalchemy


def create_enitity_types(conn: sqlalchemy.engine.base.Connection):
    """Create EntityType table"""
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS EntityType(
                Id INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                Description TEXT NOT NULL
            )
        """
    )


class EntityTypeId(IntEnum):
    """All supported types"""

    Image = 1
    Gif = 2
    Gallery = 3
    Video = 4


@dataclass
class EntityType:
    """EntityType"""

    id_: EntityTypeId
    name: str
    description: str


def insert_enitity_types(conn: sqlalchemy.engine.base.Connection):
    """Populate EntityType table"""
    conn.execute(
        """
            INSERT OR REPLACE INTO EntityType (Id, Name, Description)
            VALUES
                (1, 'image', 'Single Image'),
                (2, 'gif', 'Single Gif'),
                (3, 'gallery', 'Multiple images/files in a directory treated as a single enitity'),
                (4, 'video', 'Single video');
        """
    )
