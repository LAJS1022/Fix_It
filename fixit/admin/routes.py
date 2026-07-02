from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from fixit.users.models import User
from fixit.providers.models import Provider
from fixit.bookings.models import Booking

ns = Namespace('admin', description='Admin operations')

def admin_required():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return False
    return True

@ns.route('/users/')
class AdminUserList(Resource):
    @jwt_required()
    def get(self):
        if not admin_required():
            return {'error': 'Admin access required'}, 403
        users = User.query.all()
        return [u.to_dict() for u in users], 200

@ns.route('/users/<string:user_id>/ban')
class AdminUserBan(Resource):
    @jwt_required()
    def put(self, user_id):
        if not admin_required():
            return {'error': 'Admin access required'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if user.is_admin:
            return {'error': 'Cannot ban an admin user'}, 400

        user.is_banned = not user.is_banned
        user.update()

        status = 'banned' if user.is_banned else 'unbanned'
        return {'message': 'User ' + status + ' successfully', 'is_banned': user.is_banned}, 200

@ns.route('/providers/<string:provider_id>/verify')
class AdminProviderVerify(Resource):
    @jwt_required()
    def put(self, provider_id):
        if not admin_required():
            return {'error': 'Admin access required'}, 403

        provider = Provider.query.get(provider_id)
        if not provider:
            return {'error': 'Provider not found'}, 404

        provider.verified = not provider.verified
        provider.update()

        status = 'verified' if provider.verified else 'unverified'
        return {'message': 'Provider ' + status + ' successfully', 'verified': provider.verified}, 200

@ns.route('/bookings/')
class AdminBookingList(Resource):
    @jwt_required()
    def get(self):
        if not admin_required():
            return {'error': 'Admin access required'}, 403

        bookings = Booking.query.all()
        return [b.to_dict() for b in bookings], 200
    
