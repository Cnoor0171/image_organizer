"""Database interface"""

import sqlalchemy
from organizer.db.schema import initialize_db, EntityTypeId
from organizer.db.queries import entity
from organizer.db.queries import groups
from organizer.db.queries import groupings


class DBInstance:
    """Interface to the database """

    def __init__(self, database_file_name: str):
        self._engine = sqlalchemy.create_engine(f"sqlite:///{database_file_name}")
        with self._engine.connect() as conn:
            initialize_db(conn)

    def add_enitity(self, hash_, type_, name):
        """Add a new entity"""
        with self._engine.connect() as conn:
            return entity.insert(conn, hash_, type_, name)

    def get_all_entities(self):
        """Get all enitities"""
        with self._engine.connect() as conn:
            return entity.get_all(conn)

    def get_entity_by_id(self, ent_id: int):
        """Get one enitity by its id"""
        with self._engine.connect() as conn:
            return entity.get_by_id(conn, ent_id)

    def get_entity_by_hash(self, ent_hash: str):
        """Get one enitity by its hash"""
        with self._engine.connect() as conn:
            return entity.get_by_hash(conn, ent_hash)

    def get_all_entity_types(self):
        """Get all entity types"""
        with self._engine.connect() as conn:
            return entity.get_all_types(conn)

    def get_entity_type_by_id(self, id_: EntityTypeId):
        """Get all entity types"""
        with self._engine.connect() as conn:
            return entity.get_type_by_id(conn, id_)

    def get_all_groupings(self):
        """Get all groupings"""
        with self._engine.connect() as conn:
            return groupings.get_all(conn)

    def get_grouping_by_id(self, id_: int):
        """Get grouping by its id"""
        with self._engine.connect() as conn:
            return groupings.get_by_id(conn, id_)

    def get_all_groups(self):
        """Get all groups"""
        with self._engine.connect() as conn:
            return groups.get_all(conn)

    def get_group_by_id(self, id_: int):
        """Get one group by id"""
        with self._engine.connect() as conn:
            return groups.get_by_id(conn, id_)
