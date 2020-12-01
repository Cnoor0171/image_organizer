"""Database interface"""

import sqlalchemy
from organizer.db.schema import initialize_db
from organizer.db.queries import entity
from organizer.db.queries import groupings


class DBInstance:
    """Interface to the database """

    def __init__(self, database_file_name: str):
        self._engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
            f"sqlite:///{database_file_name}"
        )
        initialize_db(self.connect())

    def connect(self) -> sqlalchemy.engine.base.Connection:
        """Get connection to the database"""
        return self._engine.connect()

    def add_enitity(self, hash_, type_, name):
        """Add a new entity"""
        return entity.insert(self.connect(), hash_, type_, name)

    def get_enitities(self):
        """Get all enitities"""
        return entity.get_all(self.connect())

    def get_entity_by_id(self, ent_id):
        """Get one enitity"""
        return entity.get_by_id(self.connect(), ent_id)

    def get_types(self):
        """Get all types"""
        return entity.get_types(self.connect())

    def get_groupings(self):
        """Get all groupings"""
        return groupings.get_groupings(self.connect())

    def get_groups(self):
        """Get all groups"""
        return groupings.get_groups(self.connect())
