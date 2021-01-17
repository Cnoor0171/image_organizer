"""Db schema definitions for entity"""
from dataclasses import dataclass
import sqlalchemy


@dataclass
class Entity:
    """Entity"""

    id_: int
    hash_: str
    type_: int
    name: str


def create_entities(conn: sqlalchemy.engine.base.Connection):
    """Create Entity table"""
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Entity(
                Id INTEGER NOT NULL PRIMARY KEY,
                Hash TEXT NOT NULL UNIQUE,
                Type INTEGER NOT NULL REFERENCES Types(Id),
                Name TEXT
            )
        """
    )
