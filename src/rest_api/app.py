"""Rest api interface to the image organizer"""

from flask import Flask

from organizer import Organizer
from rest_api.apis import api


def get_flask_app(organizer: Organizer):
    """Get a flask rest api attached to the given organizer object"""
    app = Flask(__name__)
    app.config["organizer"] = organizer
    app.config["RESTX_VALIDATE"] = True
    app.config["RESTX_MASK_SWAGGER"] = False
    api.init_app(app)
    return app
