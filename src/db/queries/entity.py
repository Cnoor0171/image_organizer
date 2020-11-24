"""Database queries related to entities"""

from sqlalchemy.engine.base import Connection
from db.schema import Entity, Type


def insert_entity(conn: Connection, hash_, type_, name):
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

    return get_entity_by_hash(conn, hash_)


def get_entity_by_hash(conn: Connection, hash_):
    """Get entity details by its hash"""
    row = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type
            FROM Entities
            WHERE Hash = :hash
        """,
        hash_,
    ).fetchone()
    return Entity(id_=row.Id, hash_=row.Hash, type_=row.Type,)


def get_all(conn: Connection):
    """Get list of all entities"""
    res = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type
            FROM Entities
        """
    ).fetchall()

    return [Entity(id_=row.Id, hash_=row.Hash, type_=row.Type,) for row in res]


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

    return [
        Type(id_=row.Id, name=row.Name, description=row.Description,) for row in res
    ]
