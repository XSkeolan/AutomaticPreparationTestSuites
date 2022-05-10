import os

from flask import Flask
from flask_migrate import Migrate
from app.models import *
from .database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)

    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    with app.test_request_context():
        db.create_all()

    import app.authmodule.controllers as authmodule

    app.register_blueprint(authmodule.module)

    return app