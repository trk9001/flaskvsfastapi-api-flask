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

    from api.models import db
    db.init_app(app)

    from api.views import index
    app.add_url_rule('/', 'index', index)

    return app


import api.views
