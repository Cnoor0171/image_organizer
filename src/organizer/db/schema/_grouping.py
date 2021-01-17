"""Db schema definitions for grouping"""
from dataclasses import dataclass
import sqlalchemy


@dataclass
class Grouping:
    """Grouping"""

    id_: int
    name: str


def create_groupings(conn: sqlalchemy.engine.base.Connection):
    """Create Grouping table"""
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Grouping(
                Id INTEGER NOT NULL PRIMARY KEY,
                Name TEXT NOT NULL
            )
        """
    )
