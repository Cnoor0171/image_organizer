"""Rest api endpoints"""

from flask_restx import Api

from rest_api.apis import (
    entities,
    groupings,
    groups,
)
from rest_api.models.error import get_model as get_error_model
from rest_api.exceptions import ErrorResponse

api = Api(title="Image Organizer", doc="/documentation")

api.add_namespace(entities.api, "/entities")
api.add_namespace(groupings.api, "/groupings")
api.add_namespace(groups.api, "/groups")

ErrorModel = get_error_model(api)

@api.errorhandler(ErrorResponse)
@api.marshal_with(ErrorModel)
def error_handler(error):
    return error, error.code
