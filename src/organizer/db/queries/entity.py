"""Database queries related to entities"""

from sqlalchemy.engine.base import Connection
from organizer.db.schema import Entity, EntityType, EntityTypeId


def insert(conn: Connection, hash_, type_, name):
    """Insert new enitity, if the hash doesn't already exist. No-op if exists"""
    conn.execute(
        """
            INSERT INTO Entity (Hash, Type, Name)
            SELECT :hash, :type, :name
            WHERE NOT EXISTS (SELECT * FROM Entity WHERE Hash = :hash)
        """,
        hash=hash_,
        type=type_,
        name=name,
    )

    return get_by_hash(conn, hash_)


def get_by_hash(conn: Connection, hash_: str):
    """Get entity details by its hash"""
    row = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type,
                Name
            FROM Entity
            WHERE Hash = :hash
        """,
        hash=hash_,
    ).fetchone()
    return (
        Entity(id_=row.Id, hash_=row.Hash, type_=row.Type, name=row.Name)
        if row
        else None
    )


def get_by_id(conn: Connection, id_: int):
    """Get entity details by its id"""
    row = conn.execute(
        """
            SELECT
                Id,
                Hash,
                Type,
                Name
            FROM Entity
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
            FROM Entity
        """
    ).fetchall()

    return [
        Entity(id_=row.Id, hash_=row.Hash, type_=row.Type, name=row.Name) for row in res
    ]


def get_all_types(conn: Connection):
    """Get list of all types"""
    res = conn.execute(
        """
            SELECT
                Id,
                Name,
                Description
            FROM EntityType
        """
    )

    return [
        EntityType(id_=row.Id, name=row.Name, description=row.Description)
        for row in res
    ]


def get_type_by_id(conn: Connection, id_: EntityTypeId):
    """Get type by id"""
    res = conn.execute(
        """
            SELECT
                Id,
                Name,
                Description
            FROM EntityType
            WHERE Id = :id
        """,
        id=id_,
    ).fetchone()

    return EntityType(id_=res.Id, name=res.Name, description=res.Description)
