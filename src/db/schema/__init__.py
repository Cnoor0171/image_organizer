"""Database schema types and initializers"""

from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

import sqlalchemy


def initialize_db(conn: sqlalchemy.engine.base.Connection):
    """Initialize database with tables"""
    _create_entities(conn)
    _create_types(conn)
    _insert_types(conn)
    _create_groupings(conn)
    _create_group(conn)
    _create_entity_group_map(conn)


@dataclass
class Entity:
    """Entity"""

    id_: int
    hash_: str
    type_: int


def _create_entities(conn: sqlalchemy.engine.base.Connection):
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Entities(
                Id INTEGER NOT NULL PRIMARY KEY,
                Hash TEXT NOT NULL UNIQUE,
                Type INTEGER NOT NULL REFERENCES Types(Id),
                Name TEXT
            )
        """
    )


@dataclass
class Type:
    """Type"""

    id_: int
    name: str
    description: int


def _create_types(conn: sqlalchemy.engine.base.Connection):
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Types(
                Id INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL,
                Description TEXT NOT NULL
            )
        """
    )


class Types(IntEnum):
    """All supported types"""

    Image = 1
    Gif = 2
    Gallery = 3
    Video = 4


def _insert_types(conn: sqlalchemy.engine.base.Connection):
    conn.execute(
        """
            INSERT OR REPLACE INTO Types (Id, Name, Description)
            VALUES
                (1, 'image', 'Single Image'),
                (2, 'gif', 'Single Gif'),
                (3, 'gallery', 'Multiple images/files in a directory treated as a single enitity'),
                (4, 'video', 'Single video');
        """
    )


@dataclass
class Grouping:
    """Grouping"""

    id_: int
    name: str


def _create_groupings(conn: sqlalchemy.engine.base.Connection):
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Groupings(
                Id INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL
            )
        """
    )


@dataclass
class Group:
    """Group"""

    id_: int
    groupings_id: int
    name: str
    description: Optional[str]


def _create_group(conn: sqlalchemy.engine.base.Connection):
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Groups(
                Id INTEGER NOT NULL PRIMARY KEY,
                GroupingsId INTEGER NOT NULL REFERENCES Groupings(Id),
                Name TEXT NOT NULL,
                Description TEXT
            )
        """
    )


def _create_entity_group_map(conn: sqlalchemy.engine.base.Connection):
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS EntityGroupMaps(
                EntityId INTEGER NOT NULL REFERENCES Entities(Id),
                GroupId INTEGER NOT NULL REFERENCES Groups(Id)
            )
        """
    )
