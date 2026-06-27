from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from fixit.services.models import Service
from fixit.providers.models import Provider

ns = Namespace('services', description='Service operations')

service_model = ns.model('Service', {
    'category_id': fields.String(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=False),
    'price': fields.Float(required=True),
    'unit': fields.String(required=False),
    'duration_min': fields.Integer(required=False)
})

@ns.route('/')
class ServiceList(Resource):
    def get(self):
        services = Service.query.all()
        return [s.to_dict() for s in services], 200

    @jwt_required()
    @ns.expect(service_model)
    def post(self):
        current_user_id = get_jwt_identity()

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        if not provider:
            return {'error': 'You must have a provider profile to create a service'}, 403

        data = request.json
        try:
            service = Service(
                provider_id=provider.id,
                category_id=data['category_id'],
                name=data['name'],
                price=data['price'],
                description=data.get('description'),
                unit=data.get('unit'),
                duration_min=data.get('duration_min')
            )
            service.save()
            return service.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:service_id>')
class ServiceResource(Resource):
    def get(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {'error': 'Service not found'}, 404
        return service.to_dict(), 200

    @jwt_required()
    @ns.expect(service_model)
    def put(self, service_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        service = Service.query.get(service_id)
        if not service:
            return {'error': 'Service not found'}, 404

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        if not provider or service.provider_id != provider.id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        data = request.json
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.price = data.get('price', service.price)
        service.unit = data.get('unit', service.unit)
        service.duration_min = data.get('duration_min', service.duration_min)
        service.available = data.get('available', service.available)
        service.update()
        return service.to_dict(), 200

    @jwt_required()
    def delete(self, service_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        service = Service.query.get(service_id)
        if not service:
            return {'error': 'Service not found'}, 404

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        if not provider or service.provider_id != provider.id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        service.delete()
        return {'message': 'Service deleted successfully'}, 200
