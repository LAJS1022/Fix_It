from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from fixit.favorites.models import Favorite
from fixit.providers.models import Provider

ns = Namespace('favorites', description='Favorite operations')

favorite_model = ns.model('Favorite', {
    'provider_id': fields.String(required=True)
})

@ns.route('/')
class FavoriteList(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        favorites = Favorite.query.filter_by(client_id=current_user_id).all()
        return [f.to_dict() for f in favorites], 200

    @jwt_required()
    @ns.expect(favorite_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        provider = Provider.query.get(data['provider_id'])
        if not provider:
            return {'error': 'Provider not found'}, 404

        existing = Favorite.query.filter_by(
            client_id=current_user_id,
            provider_id=data['provider_id']
        ).first()
        if existing:
            return {'error': 'Provider already in favorites'}, 400

        favorite = Favorite(
            client_id=current_user_id,
            provider_id=data['provider_id']
        )
        favorite.save()
        return favorite.to_dict(), 201

@ns.route('/<string:favorite_id>')
class FavoriteResource(Resource):
    @jwt_required()
    def delete(self, favorite_id):
        current_user_id = get_jwt_identity()

        favorite = Favorite.query.get(favorite_id)
        if not favorite:
            return {'error': 'Favorite not found'}, 404

        if favorite.client_id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        favorite.delete()
        return {'message': 'Favorite removed successfully'}, 200
