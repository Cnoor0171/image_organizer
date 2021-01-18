"""Database interface"""

import sqlalchemy
from organizer.db.schema import initialize_db, EntityTypeId
import organizer.db.queries as query


class DBInstance:
    """Interface to the database """

    def __init__(self, database_file_name: str):
        self._engine = sqlalchemy.create_engine(f"sqlite:///{database_file_name}")
        with self._engine.connect() as conn:
            initialize_db(conn)

    def add_enitity(self, hash_, type_, name):
        """Add a new entity"""
        with self._engine.connect() as conn:
            return query.entity.insert(conn, hash_, type_, name)

    def get_all_entities(self, get_groups: bool = False):
        """Get all enitities"""
        with self._engine.connect() as conn:
            entities = query.entity.get_all(conn)
            if get_groups:
                groups = query.group.get_all(conn)
                mapping = query.group.get_all_map_from_entity(conn)
                for ent_id, ent in entities.items():
                    ent_groups = [
                        groups[group_id] for group_id in mapping.get(ent_id, [])
                    ]
                    ent.groups = ent_groups
            return entities

    def get_entity_by_id(self, ent_id: int, get_groups: bool = False):
        """Get one enitity by its id"""
        with self._engine.connect() as conn:
            entity = query.entity.get_by_id(conn, ent_id)
            if not entity:
                return None
            if get_groups:
                group_ids = query.group.get_map_from_entity(conn, ent_id)
                groups = query.group.get_by_ids(conn, group_ids)
                entity.groups = list(groups.values())
            return entity

    def get_entity_by_hash(self, ent_hash: str):
        """Get one enitity by its hash"""
        with self._engine.connect() as conn:
            return query.entity.get_by_hash(conn, ent_hash)

    def get_all_entity_types(self):
        """Get all entity types"""
        with self._engine.connect() as conn:
            return query.entity.get_all_types(conn)

    def get_entity_type_by_id(self, id_: EntityTypeId):
        """Get all entity types"""
        with self._engine.connect() as conn:
            return query.entity.get_type_by_id(conn, id_)

    def get_all_groupings(self):
        """Get all groupings"""
        with self._engine.connect() as conn:
            return query.grouping.get_all(conn)

    def get_grouping_by_id(self, id_: int):
        """Get grouping by its id"""
        with self._engine.connect() as conn:
            return query.grouping.get_by_id(conn, id_)

    def get_all_groups(self):
        """Get all groups"""
        with self._engine.connect() as conn:
            return query.group.get_all(conn)

    def get_group_by_id(self, id_: int):
        """Get one group by id"""
        with self._engine.connect() as conn:
            return query.group.get_by_id(conn, id_)
