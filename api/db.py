import json
import sys
from pathlib import Path
from typing import Any

from flask import current_app, Flask
from flask.cli import cli
from flask_migrate import Migrate
from flask_sqlalchemy import SessionBase, SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


@cli.command()
def seed_db():
    """Seed the database if it is unpopulated."""
    from api.models import Product

    if Product.query.count():
        print('[INFO] The database is already populated.', file=sys.stderr)
        return

    app: Flask = current_app
    root_path = Path(app.root_path).parent
    data_file_path = root_path / 'seed-data.json'
    with open(data_file_path) as fp:
        data = json.load(fp)

    session: SessionBase = db.session

    for item in data:
        for x in item['products']:  # type: dict[str, str]
            fields: dict[str, Any] = x.copy()
            fields.update(price=float(x['price'].replace(',', '')))
            p = Product(category=item['category'], **fields)
            session.add(p)

    session.commit()
    print('[INFO] The database has been seeded.', file=sys.stderr)
