from database import db, bcrypt
from fixit.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(10), nullable=False, default='client')
    avatar_url = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, phone=None, role='client', city=None, is_admin=False):
        if not email or '@' not in email:
            raise ValueError('Invalid email address')
        if not password:
            raise ValueError('Password is required')
        if role not in ['client', 'provider']:
            raise ValueError('Role must be client or provider')

        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.phone = phone
        self.role = role
        self.city = city
        self.is_admin = is_admin

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'avatar_url': self.avatar_url,
            'city': self.city,
            'is_admin': self.is_admin,
            'is_banned': self.is_banned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
