"""Enitity endpoints"""

from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse

from organizer import Organizer
from rest_api.utils.parsers import OptFields

api = Namespace("Entities", description="Entity Details")

EntityModel = api.model(
    "Entity",
    {
        "id": fields.Integer(readonly=True, attribute="id_"),
        "name": fields.String(),
        "type": fields.Integer(attribute="type_"),
        "groups": fields.List(
            fields.Nested(
                api.model(
                    "EntityGroups",
                    {
                        "id": fields.Integer(attribute="id_"),
                        "name": fields.String(readonly=True),
                    },
                )
            ),
        ),
    },
)


@api.route("/")
class EntityList(Resource):
    """Manipulate list of entities"""

    GetQueryParams = reqparse.RequestParser()
    GetQueryParams.add_argument(
        "opt-fields",
        type=OptFields,
        location="args",
        help="List of optional fields to include. Currently supports: groups",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._organizer: Organizer = current_app.config["organizer"]

    @api.marshal_with(EntityModel, as_list=True)
    @api.expect(GetQueryParams)
    def get(self):
        """List entities"""
        q_params = self.GetQueryParams.parse_args()
        q_params["opt-fields"] = q_params["opt-fields"] or OptFields()
        get_groups = "groups" in q_params["opt-fields"].fields
        entities = self._organizer.get_all_entities(get_groups=get_groups)
        return list(entities.values())


@api.route("/<int:entity_id>")
class Entity(Resource):
    """Manipulate single entity"""

    GetQueryParams = reqparse.RequestParser()
    GetQueryParams.add_argument(
        "opt-fields",
        type=OptFields,
        location="args",
        help="List of optional fields to include. Currently supports: groups",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._organizer: Organizer = current_app.config["organizer"]

    @api.marshal_with(EntityModel)
    @api.expect(GetQueryParams)
    @api.doc(params={"entity_id": "Enitity Id to retrieve"})
    def get(self, entity_id):
        """Get one entity by id"""
        q_params = self.GetQueryParams.parse_args()
        q_params["opt-fields"] = q_params["opt-fields"] or OptFields()
        get_groups = "groups" in q_params["opt-fields"].fields
        entity = self._organizer.get_entity_by_id(entity_id, get_groups=get_groups)
        return entity
