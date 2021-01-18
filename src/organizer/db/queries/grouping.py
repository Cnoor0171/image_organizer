"""Database queries related to groupings"""

from sqlalchemy.engine.base import Connection

from organizer.db.schema import Grouping


def get_all(conn: Connection):
    """Get list of all groupings"""
    res = conn.execute(
        """
            SELECT
                Id,
                Name
            FROM Grouping
        """
    ).fetchall()

    return [
        Grouping(
            id_=row.Id,
            name=row.Name,
        )
        for row in res
    ]


def get_by_id(conn: Connection, id_: int):
    """Get grouping by its id"""
    res = conn.execute(
        """
            SELECT
                Id,
                Name
            FROM Grouping
            WHERE Id = :id
        """,
        id=id_,
    ).fetchone()

    return Grouping(id_=res.Id, name=res.Name)
