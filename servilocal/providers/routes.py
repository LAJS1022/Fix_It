from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from servilocal.providers.models import Provider
from database import db

ns = Namespace('providers', description='Provider operations')

provider_model = ns.model('Provider', {
    'bio': fields.String(required=False),
    'experience_years': fields.Integer(required=False),
    'price_min': fields.Float(required=False),
    'price_max': fields.Float(required=False),
    'service_zone': fields.String(required=False),
    'latitude': fields.Float(required=False),
    'longitude': fields.Float(required=False)
})

@ns.route('/')
class ProviderList(Resource):
    def get(self):
        providers = Provider.query.all()
        return [p.to_dict() for p in providers], 200

    @jwt_required()
    @ns.expect(provider_model)
    def post(self):
        current_user_id = get_jwt_identity()

        existing = Provider.query.filter_by(user_id=current_user_id).first()
        if existing:
            return {'error': 'Provider profile already exists'}, 400

        data = request.json
        try:
            provider = Provider(
                user_id=current_user_id,
                bio=data.get('bio'),
                experience_years=data.get('experience_years'),
                price_min=data.get('price_min'),
                price_max=data.get('price_max'),
                service_zone=data.get('service_zone'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            provider.save()
            return provider.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:provider_id>')
class ProviderResource(Resource):
    def get(self, provider_id):
        provider = Provider.query.get(provider_id)
        if not provider:
            return {'error': 'Provider not found'}, 404
        return provider.to_dict(), 200

    @jwt_required()
    @ns.expect(provider_model)
    def put(self, provider_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        provider = Provider.query.get(provider_id)
        if not provider:
            return {'error': 'Provider not found'}, 404

        if provider.user_id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        data = request.json
        provider.bio = data.get('bio', provider.bio)
        provider.experience_years = data.get('experience_years', provider.experience_years)
        provider.price_min = data.get('price_min', provider.price_min)
        provider.price_max = data.get('price_max', provider.price_max)
        provider.service_zone = data.get('service_zone', provider.service_zone)
        provider.latitude = data.get('latitude', provider.latitude)
        provider.longitude = data.get('longitude', provider.longitude)
        provider.update()
        return provider.to_dict(), 200

@ns.route('/<string:provider_id>/gallery')
class ProviderGallery(Resource):
    def get(self, provider_id):
        from servilocal.gallery.models import Gallery
        provider = Provider.query.get(provider_id)
        if not provider:
            return {'error': 'Provider not found'}, 404
        gallery = Gallery.query.filter_by(provider_id=provider_id).all()
        return [g.to_dict() for g in gallery], 200
