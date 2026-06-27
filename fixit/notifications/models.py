from database import db
from fixit.base_model import BaseModel

class Notification(BaseModel):
    __tablename__ = 'notifications'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def __init__(self, user_id, type, message):
        super().__init__()
        self.user_id = user_id
        self.type = type
        self.message = message

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
