from flask_restx import fields

def get_model(api):
    return api.model(
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
