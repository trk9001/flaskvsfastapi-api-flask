import os

from flask import Flask


def create_app(*args, **kwargs):
    """Flask application factory."""
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py')

    from api.db import db, migrate, seed_db
    db.init_app(app)
    migrate.init_app(app, db)
    app.cli.add_command(seed_db, 'seed-db')

    from api.models import ma
    ma.init_app(app)

    from api.views import api
    api.init_app(app)

    return app


import api.views
import api.models
