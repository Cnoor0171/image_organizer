"""Database queries related to entities"""

from sqlalchemy.engine.base import Connection
from organizer.db.schema import Entity, Type


def insert(conn: Connection, hash_, type_, name):
    """Insert new enitity, if the hash doesn't already exist. No-op if exists"""
    conn.execute(
        """
            INSERT INTO Entities (Hash, Type, Name)
            SELECT :hash, :type, :name
            WHERE NOT EXISTS (SELECT * FROM Entities WHERE Hash = :hash)
        """,
        hash=hash_,
        type=type_,
        name=name,
    )

    return get_by_hash(conn, hash_)


def get_by_hash(conn: Connection, hash_):
    """Get entity details by its hash"""
    row = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type,
                Name
            FROM Entities
            WHERE Hash = :hash
        """,
        hash=hash_,
    ).fetchone()
    return (
        Entity(id_=row.Id, hash_=row.Hash, type_=row.Type, name=row.Name)
        if row
        else None
    )


def get_by_id(conn: Connection, id_):
    """Get entity details by its id"""
    row = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type,
                Name
            FROM Entities
            WHERE Id = :id
        """,
        id=id_,
    ).fetchone()
    return (
        Entity(id_=row.Id, hash_=row.Hash, type_=row.Type, name=row.Name)
        if row
        else None
    )


def get_all(conn: Connection):
    """Get list of all entities"""
    res = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type,
                Name
            FROM Entities
        """
    ).fetchall()

    return [
        Entity(id_=row.Id, hash_=row.Hash, type_=row.Type, name=row.Name) for row in res
    ]


def get_types(conn: Connection):
    """Get list of all types"""
    res = conn.execute(
        """
            SELECT
                Id,
                Name,
                Description
            FROM Types
        """
    )

    return [Type(id_=row.Id, name=row.Name, description=row.Description) for row in res]
