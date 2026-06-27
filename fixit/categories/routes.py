from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from fixit.categories.models import Category

ns = Namespace('categories', description='Category operations')

category_model = ns.model('Category', {
    'name': fields.String(required=True),
    'slug': fields.String(required=True),
    'icon': fields.String(required=False),
    'description': fields.String(required=False)
})

@ns.route('/')
class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        return [c.to_dict() for c in categories], 200

    @jwt_required()
    @ns.expect(category_model)
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        data = request.json
        try:
            category = Category(
                name=data['name'],
                slug=data['slug'],
                icon=data.get('icon'),
                description=data.get('description')
            )
            category.save()
            return category.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:category_id>')
class CategoryResource(Resource):
    def get(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 404
        return category.to_dict(), 200

    @jwt_required()
    @ns.expect(category_model)
    def put(self, category_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 404

        data = request.json
        category.name = data.get('name', category.name)
        category.slug = data.get('slug', category.slug)
        category.icon = data.get('icon', category.icon)
        category.description = data.get('description', category.description)
        category.update()
        return category.to_dict(), 200

    @jwt_required()
    def delete(self, category_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 404

        category.delete()
        return {'message': 'Category deleted successfully'}, 200

@ns.route('/<string:category_id>/providers')
class CategoryProviders(Resource):
    def get(self, category_id):
        from fixit.providers.models import Provider
        from fixit.services.models import Service
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 404
        services = Service.query.filter_by(category_id=category_id).all()
        provider_ids = list(set(s.provider_id for s in services))
        providers = Provider.query.filter(Provider.id.in_(provider_ids)).all()
        return [p.to_dict() for p in providers], 200
