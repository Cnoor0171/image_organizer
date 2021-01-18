"""SQL queries about groups"""
from typing import Dict, List, Optional

from sqlalchemy.engine.base import Connection
from sqlalchemy import text, bindparam

from organizer.db.schema import Group


def get_all(conn: Connection) -> Dict[int, Group]:
    """Get dict of all groups"""
    res = conn.execute(
        """
            SELECT
                Id,
                GroupingId,
                Name,
                Description
            FROM 'Group'
        """
    ).fetchall()

    return {
        row.Id: Group(
            id_=row.Id,
            name=row.Name,
            groupings_id=row.GroupingId,
            description=row.Description,
        )
        for row in res
    }


def get_by_id(conn: Connection, id_: int) -> Optional[Group]:
    """Get group by group id"""
    res = conn.execute(
        """
            SELECT
                Id,
                GroupingId,
                Name,
                Description
            FROM 'Group'
            WHERE Id = :id
        """,
        id=id_,
    ).fetchone()

    return Group(
        id_=res.Id,
        name=res.Name,
        groupings_id=res.GroupingId,
        description=res.Description,
    ) if res else None


def get_by_ids(conn: Connection, ids: List[int]) -> Dict[int, Group]:
    """Get dict of groups by group ids"""
    query = text(
        """
        SELECT
            Id,
            GroupingId,
            Name,
            Description
        FROM 'Group'
        WHERE Id IN :ids
    """
    )
    query = query.bindparams(bindparam("ids", expanding=True))
    params = {"ids": ids}
    res = conn.execute(query, params).fetchall()

    return {
        row.Id: Group(
            id_=row.Id,
            name=row.Name,
            groupings_id=row.GroupingId,
            description=row.Description,
        )
        for row in res
    }


def get_all_map_from_entity(conn: Connection) -> Dict[int, List[int]]:
    """Get all entity to list of groups mapping"""
    res = conn.execute(
        """
            SELECT
                EntityId,
                GroupId
            FROM EntityGroupMap
        """,
    ).fetchall()

    mappings: Dict[int, List[int]] = {}
    for row in res:
        mappings.setdefault(row.EntityId, []).append(row.GroupId)
    return mappings


def get_map_from_entity(conn: Connection, entity_id: int) -> List[int]:
    """Get entity to list of groups mapping for one enitity"""
    res = conn.execute(
        """
            SELECT
                GroupId
            FROM EntityGroupMap
            WHERE EntityId = :entity_id
        """,
        entity_id=entity_id,
    ).fetchall()

    return [row.GroupId for row in res]
