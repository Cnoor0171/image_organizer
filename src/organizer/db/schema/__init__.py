"""Database schema types and initializers"""

import sqlalchemy

from ._entity import Entity, create_entities
from ._entity_type import (
    EntityType,
    EntityTypeId,
    create_enitity_types,
    insert_enitity_types,
)
from ._grouping import Grouping, create_groupings
from ._group import Group, create_group, create_entity_group_map


def initialize_db(conn: sqlalchemy.engine.base.Connection):
    """Initialize database with tables"""
    create_entities(conn)
    create_enitity_types(conn)
    insert_enitity_types(conn)
    create_groupings(conn)
    create_group(conn)
    create_entity_group_map(conn)
