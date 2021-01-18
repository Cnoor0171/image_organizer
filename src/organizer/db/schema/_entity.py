"""Db schema definitions for entity"""
from dataclasses import dataclass
from typing import Optional, List

import sqlalchemy

from ._entity_type import EntityTypeId
from ._group import Group


@dataclass
class Entity:
    """Entity"""

    id_: int
    hash_: str
    type_: EntityTypeId
    name: str
    groups: Optional[List[Group]] = None


def create_entities(conn: sqlalchemy.engine.base.Connection):
    """Create Entity table"""
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Entity(
                Id INTEGER NOT NULL PRIMARY KEY,
                Hash TEXT NOT NULL UNIQUE,
                Type INTEGER NOT NULL REFERENCES EntityType(Id),
                Name TEXT
            )
        """
    )
