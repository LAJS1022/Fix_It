from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from servilocal.bookings.models import Booking, VALID_STATUSES
from servilocal.services.models import Service
from servilocal.providers.models import Provider
from datetime import datetime

ns = Namespace('bookings', description='Booking operations')

booking_model = ns.model('Booking', {
    'provider_id': fields.String(required=True),
    'service_id': fields.String(required=True),
    'date': fields.String(required=True),
    'address': fields.String(required=True),
    'notes': fields.String(required=False)
})

status_model = ns.model('Status', {
    'status': fields.String(required=True)
})

@ns.route('/')
class BookingList(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if claims.get('is_admin'):
            bookings = Booking.query.all()
        elif claims.get('role') == 'provider':
            provider = Provider.query.filter_by(user_id=current_user_id).first()
            bookings = Booking.query.filter_by(provider_id=provider.id).all() if provider else []
        else:
            bookings = Booking.query.filter_by(client_id=current_user_id).all()

        return [b.to_dict() for b in bookings], 200

    @jwt_required()
    @ns.expect(booking_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        service = Service.query.get(data['service_id'])
        if not service:
            return {'error': 'Service not found'}, 404

        provider = Provider.query.get(data['provider_id'])
        if not provider:
            return {'error': 'Provider not found'}, 404

        if provider.user_id == current_user_id:
            return {'error': 'You cannot book your own service'}, 400

        try:
            booking = Booking(
                client_id=current_user_id,
                provider_id=data['provider_id'],
                service_id=data['service_id'],
                date=datetime.fromisoformat(data['date']),
                address=data['address'],
                total_price=service.price,
                notes=data.get('notes')
            )
            booking.save()
            return booking.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:booking_id>')
class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        booking = Booking.query.get(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        is_provider = provider and booking.provider_id == provider.id

        if booking.client_id != current_user_id and not is_provider and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        return booking.to_dict(), 200

@ns.route('/<string:booking_id>/status')
class BookingStatus(Resource):
    @jwt_required()
    @ns.expect(status_model)
    def put(self, booking_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        booking = Booking.query.get(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        is_provider = provider and booking.provider_id == provider.id

        if not is_provider and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        data = request.json
        if data['status'] not in VALID_STATUSES:
            return {'error': 'Invalid status'}, 400

        booking.status = data['status']
        booking.update()
        return booking.to_dict(), 200
