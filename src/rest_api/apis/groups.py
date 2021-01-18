"""Group endpoints"""

from flask import current_app
from flask_restx import Namespace, Resource

from organizer import Organizer
from rest_api.constants.http import Status
from rest_api.exceptions import ErrorResponse
from rest_api.models.group import get_model

api = Namespace("Groups", description="Group Details")
GroupModel = get_model(api)

@api.route("/")
class GroupList(Resource):
    """Manipulate list of groups"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._organizer: Organizer = current_app.config["organizer"]

    @api.marshal_with(GroupModel, as_list=True)
    def get(self):
        """List groups"""
        groups = self._organizer.get_all_groups()
        return list(groups.values())


class Error:
    def __init__(self, code, message):
        self.code = code
        self.message = message

@api.route("/<int:group_id>")
class Group(Resource):
    """Manipulate single group"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._organizer: Organizer = current_app.config["organizer"]

    @api.marshal_with(GroupModel)
    @api.doc(params={"group_id": "Group id to retrieve"})
    def get(self, group_id):
        """Get one group by id"""
        group = self._organizer.get_group_by_id(group_id)
        if not group:
            raise ErrorResponse(Status.NOT_FOUND, f"Group {group_id} not found")
        return group
