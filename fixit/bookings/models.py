from database import db
from fixit.base_model import BaseModel

VALID_STATUSES = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']

class Booking(BaseModel):
    __tablename__ = 'bookings'

    client_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.String(36), db.ForeignKey('providers.id'), nullable=False)
    service_id = db.Column(db.String(36), db.ForeignKey('services.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    total_price = db.Column(db.Float, nullable=False)

    client = db.relationship('User', backref=db.backref('bookings', lazy=True))
    review = db.relationship('Review', backref='booking', uselist=False, cascade='all, delete-orphan')

    def __init__(self, client_id, provider_id, service_id, date, address, total_price, notes=None):
        if not address:
            raise ValueError('Booking must have an address')
        if total_price < 0:
            raise ValueError('Total price must be non-negative')

        super().__init__()
        self.client_id = client_id
        self.provider_id = provider_id
        self.service_id = service_id
        self.date = date
        self.address = address
        self.total_price = total_price
        self.notes = notes
        self.status = 'pending'

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'provider_id': self.provider_id,
            'service_id': self.service_id,
            'status': self.status,
            'date': self.date.isoformat(),
            'address': self.address,
            'notes': self.notes,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
