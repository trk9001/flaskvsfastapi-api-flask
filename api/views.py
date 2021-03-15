from flask import request
from flask_restful import abort, Api, Resource, reqparse

from api.db import db
from api.models import Product, product_schema, products_schema


class ProductListResource(Resource):
    """A resource for the list of Products."""
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products)

    def post(self):
        product = Product(
            name=request.json['name'],
            category=request.json['category'] or None,
            amount=request.json['amount'],
            price=request.json['amount'],
            image_source=request.json['image_source'] or None,
        )
        db.session.add(product)
        db.session.commit()
        return product_schema.dump(product)


class ProductResource(Resource):
    """The Product model's DAO."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('category')
        self.parser.add_argument('amount')
        self.parser.add_argument('price')
        self.parser.add_argument('image_source')

    @staticmethod
    def product_or_abort(product_id):
        product = Product.query.get(product_id)
        if product is None:
            abort(404, message=f'Product with id [{product_id}] doesn\'t exist')
        return product

    def get(self, product_id):
        product = self.product_or_abort(product_id)
        return product_schema.dump(product)

    def delete(self, product_id):
        product = self.product_or_abort(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

    def put(self, product_id):
        args = self.parser.parse_args()
        data = dict(
            name=args['name'],
            category=args['category'] or None,
            amount=args['amount'],
            price=args['amount'],
            image_source=args['image_source'] or None,
        )
        rows = Product.query.filter_by(id=product_id).update(data)
        if rows:
            product = Product.query.get(product_id)
        else:
            product = Product(**data)
            db.session.add(product)
        db.session.commit()
        return product_schema.dump(product), 201


api = Api(prefix='/api/v1')
api.add_resource(ProductListResource, '/products/')
api.add_resource(ProductResource, '/products/<int:product_id>')
