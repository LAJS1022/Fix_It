from database import db
from fixit.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.id'), nullable=False)
    client_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.String(36), db.ForeignKey('providers.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=True)

    def __init__(self, booking_id, client_id, provider_id, rating, comment=None):
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')

        super().__init__()
        self.booking_id = booking_id
        self.client_id = client_id
        self.provider_id = provider_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'client_id': self.client_id,
            'provider_id': self.provider_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
