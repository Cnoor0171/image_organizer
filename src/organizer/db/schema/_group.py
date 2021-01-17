"""Db schema definitions for group"""
from dataclasses import dataclass
from typing import Optional
import sqlalchemy


@dataclass
class Group:
    """Group"""

    id_: int
    groupings_id: int
    name: str
    description: Optional[str]


def create_group(conn: sqlalchemy.engine.base.Connection):
    """Create Group table"""
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS 'Group'(
                Id INTEGER NOT NULL PRIMARY KEY,
                GroupingId INTEGER NOT NULL REFERENCES Grouping(Id),
                Name TEXT NOT NULL,
                Description TEXT
            )
        """
    )


def create_entity_group_map(conn: sqlalchemy.engine.base.Connection):
    """Create EntityGroupMap table"""
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS EntityGroupMap(
                EntityId INTEGER NOT NULL REFERENCES Entities(Id),
                GroupId INTEGER NOT NULL REFERENCES Groups(Id)
            )
        """
    )
