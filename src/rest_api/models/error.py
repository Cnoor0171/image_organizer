from flask_restx import fields

def get_model(api):
    return api.model(
        "Error",
        {
            "code": fields.Integer(readonly=True),
            "message": fields.String(readonly=True),
        }
    )
