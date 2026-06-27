from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db, bcrypt
from fixit.users.models import User

ns = Namespace('auth', description='Authentication operations')

register_model = ns.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'phone': fields.String(required=False),
    'role': fields.String(required=False),
    'city': fields.String(required=False)
})

login_model = ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@ns.route('/register')
class Register(Resource):
    @ns.expect(register_model)
    def post(self):
        data = request.json

        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already registered'}, 400

        try:
            user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
                phone=data.get('phone'),
                role=data.get('role', 'client'),
                city=data.get('city')
            )
            user.save()
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json

        user = User.query.filter_by(email=data.get('email')).first()

        if not user or not user.verify_password(data.get('password')):
            return {'error': 'Invalid email or password'}, 401

        if user.is_banned:
            return {'error': 'Your account has been banned'}, 403

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'is_admin': user.is_admin,
                'role': user.role,
                'email': user.email
            }
        )

        return {
            'access_token': access_token,
            'user_id': user.id,
            'role': user.role,
            'is_admin': user.is_admin
        }, 200

@ns.route('/me')
class Me(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
