"""Group endpoints"""

from flask_restx import Namespace, Resource

api = Namespace(__name__, description="Entity Details")


@api.route("/")
class GroupList(Resource):
    """Manipulate list of groups"""

    def get(self, entity_id):
        """List all tasks"""
        return ["sadf", entity_id]


@api.route("/<entity_id>")
class Group(Resource):
    """Manipulate single group"""

    def get(self, entity_id):
        """List all tasks"""
        return ["sadf", entity_id]
