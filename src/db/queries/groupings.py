"""Database queries related to groupings"""

from sqlalchemy.engine.base import Connection

from db.schema import Grouping, Group


def get_groupings(conn: Connection):
    """Get list of all groupings"""
    res = conn.execute(
        """
            SELECT
                Id,
                Name
            FROM Groupings
        """
    ).fetchall()

    return [Grouping(id_=row.Id, name=row.Name,) for row in res]


def get_groups(conn: Connection):
    """Get list of all groups"""
    res = conn.execute(
        """
            SELECT
                Id,
                GroupingsId,
                Name,
                Description
            FROM Groups
        """
    ).fetchall()

    return [
        Group(
            id_=row.Id,
            name=row.Name,
            groupings_id=row.GroupingsId,
            description=row.Description,
        )
        for row in res
    ]
