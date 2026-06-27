from database import db
from fixit.base_model import BaseModel

class Favorite(BaseModel):
    __tablename__ = 'favorites'

    client_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.String(36), db.ForeignKey('providers.id'), nullable=False)

    client = db.relationship('User', backref=db.backref('favorites', lazy=True))
    provider = db.relationship('Provider', backref=db.backref('favorited_by', lazy=True))

    def __init__(self, client_id, provider_id):
        super().__init__()
        self.client_id = client_id
        self.provider_id = provider_id

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'provider_id': self.provider_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
