"""Enitity endpoints"""

from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse

from organizer import Organizer
from rest_api.utils.parsers import OptFields

api = Namespace("Entities", description="Entity Details")

EntityModel = api.model(
    "Entity",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(),
        "type": fields.String(),
        "groupings": fields.List(
            fields.Nested(
                api.model(
                    "EntityGrouping",
                    {
                        "id": fields.Integer(),
                        "name": fields.String(readonly=True),
                        "groups": fields.List(
                            fields.Nested(
                                api.model(
                                    "EntityGroupingGroup",
                                    {
                                        "id": fields.Integer(),
                                        "name": fields.String(readonly=True),
                                    },
                                )
                            )
                        ),
                    },
                )
            )
        ),
    },
)

EntityQueryParams = reqparse.RequestParser()
EntityQueryParams.add_argument(
    "opt-fields", type=OptFields, location="args",
)


@api.route("/")
class EntityList(Resource):
    """Manipulate list of entities"""

    def get(self):
        """List entities"""
        return ["sadf"]

    @api.expect(EntityModel)
    @api.response(204, "No Content")
    def post(self):
        """Create a new task"""
        return "", 204


@api.route("/<int:entity_id>")
class Entity(Resource):
    """Manipulate single entity"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._organizer: Organizer = current_app.config["organizer"]

    @api.doc(
        params={
            "entity_id": "Enitity Id to retrieve",
            "opt-fields": "Optional fields to include in the response",
        }
    )
    @api.expect(EntityQueryParams)
    @api.marshal_with(EntityModel)
    def get(self, entity_id):
        """Get one entity by id"""
        entity = self._organizer.get_entity_by_id(entity_id)
        query_params = EntityQueryParams.parse_args()
        opt_fields = query_params["opt-fields"] or OptFields()
        if "groupings" in opt_fields.fields:
            print("here")
        return {
            "id": entity.id_,
            "name": entity.name,
            "type": entity.type_,
        }

    def delete(self, entity_id):
        """Delete one entity by id"""

    def put(self, entity_id):
        """Edit one entity by id, replacing all information"""

    def patch(self, entity_id):
        """Edit one entity by id, replacing only given information"""
