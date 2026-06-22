from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from servilocal.users.models import User

ns = Namespace('users', description='User operations')

user_model = ns.model('User', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'phone': fields.String(required=False),
    'city': fields.String(required=False),
    'avatar_url': fields.String(required=False)
})

@ns.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @ns.expect(user_model)
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if current_user_id != user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.json
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        user.city = data.get('city', user.city)
        user.avatar_url = data.get('avatar_url', user.avatar_url)
        user.update()
        return user.to_dict(), 200

    @jwt_required()
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if current_user_id != user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user.delete()
        return {'message': 'User deleted successfully'}, 200
