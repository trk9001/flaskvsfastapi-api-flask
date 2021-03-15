from datetime import datetime

from api import db


class Product(db.Model):
    """Model representing a product."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(250),
        nullable=False,
    )
    category = db.Column(
        db.String(250),
        nullable=True,
    )
    amount = db.Column(
        db.String(250),
        nullable=True,
    )
    price = db.Column(
        db.Float(precision=2),
        nullable=False,
    )
    image_source = db.Column(
        db.String(250),
        nullable=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now,
    )

    def __repr__(self):
        return f'<Product {self.name}>'
