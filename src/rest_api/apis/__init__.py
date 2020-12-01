"""Rest api endpoints"""

from flask_restx import Api

from rest_api.apis import (
    entities,
    groupings,
    groups,
)

api = Api(title="Image Organizer", doc="/documentation")

api.add_namespace(entities.api, "/entities")
api.add_namespace(groupings.api, "/groupings")
api.add_namespace(groups.api, "/groups")
