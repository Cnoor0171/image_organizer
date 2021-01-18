from flask_restx import fields

def get_model(api):
    return api.model(
        "Group",
        {
            "id": fields.Integer(readonly=True, attribute="id_"),
            "name": fields.String(),
            "description": fields.String(),
        },
    )
