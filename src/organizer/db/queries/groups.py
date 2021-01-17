"""SQL queries about groups"""
from sqlalchemy.engine.base import Connection

from organizer.db.schema import Group


def get_all(conn: Connection):
    """Get list of all groups"""
    res = conn.execute(
        """
            SELECT
                Id,
                GroupingsId,
                Name,
                Description
            FROM Group
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


def get_by_id(conn: Connection, id_: int):
    """Get group by group id"""
    res = conn.execute(
        """
            SELECT
                Id,
                GroupingsId,
                Name,
                Description
            FROM Group
            WHERE Id = :id
        """,
        id=id_,
    ).fetchone()

    return Group(
        id_=res.Id,
        name=res.Name,
        groupings_id=res.GroupingsId,
        description=res.Description,
    )
