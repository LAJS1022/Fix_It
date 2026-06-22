from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from servilocal.reviews.models import Review
from servilocal.bookings.models import Booking
from servilocal.providers.models import Provider

ns = Namespace('reviews', description='Review operations')

review_model = ns.model('Review', {
    'booking_id': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String(required=False)
})

@ns.route('/')
class ReviewList(Resource):
    def get(self):
        reviews = Review.query.all()
        return [r.to_dict() for r in reviews], 200

    @jwt_required()
    @ns.expect(review_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        booking = Booking.query.get(data['booking_id'])
        if not booking:
            return {'error': 'Booking not found'}, 404

        if booking.client_id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        if booking.status != 'completed':
            return {'error': 'You can only review completed bookings'}, 400

        existing = Review.query.filter_by(booking_id=data['booking_id']).first()
        if existing:
            return {'error': 'You have already reviewed this booking'}, 400

        try:
            review = Review(
                booking_id=data['booking_id'],
                client_id=current_user_id,
                provider_id=booking.provider_id,
                rating=data['rating'],
                comment=data.get('comment')
            )
            review.save()

            provider = Provider.query.get(booking.provider_id)
            if provider:
                provider.update_rating()

            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        review = Review.query.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.client_id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        provider = Provider.query.get(review.provider_id)
        review.delete()

        if provider:
            provider.update_rating()

        return {'message': 'Review deleted successfully'}, 200
