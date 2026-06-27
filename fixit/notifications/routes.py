from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from fixit.notifications.models import Notification
from database import db

ns = Namespace('notifications', description='Notification operations')

@ns.route('/')
class NotificationList(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        notifications = Notification.query.filter_by(
            user_id=current_user_id
        ).order_by(Notification.created_at.desc()).all()
        return [n.to_dict() for n in notifications], 200

@ns.route('/<string:notification_id>/read')
class NotificationRead(Resource):
    @jwt_required()
    def put(self, notification_id):
        current_user_id = get_jwt_identity()

        notification = Notification.query.get(notification_id)
        if not notification:
            return {'error': 'Notification not found'}, 404

        if notification.user_id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        notification.read = True
        notification.update()
        return notification.to_dict(), 200

@ns.route('/read-all')
class NotificationReadAll(Resource):
    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()

        notifications = Notification.query.filter_by(
            user_id=current_user_id,
            read=False
        ).all()

        for notification in notifications:
            notification.read = True

        db.session.commit()
        return {'message': 'All notifications marked as read'}, 200

@ns.route('/<string:notification_id>')
class NotificationResource(Resource):
    @jwt_required()
    def delete(self, notification_id):
        current_user_id = get_jwt_identity()

        notification = Notification.query.get(notification_id)
        if not notification:
            return {'error': 'Notification not found'}, 404

        if notification.user_id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        notification.delete()
        return {'message': 'Notification deleted successfully'}, 200
