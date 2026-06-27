from database import db
from fixit.base_model import BaseModel

class Service(BaseModel):
    __tablename__ = 'services'

    provider_id = db.Column(db.String(36), db.ForeignKey('providers.id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    duration_min = db.Column(db.Integer, nullable=True)
    available = db.Column(db.Boolean, default=True)

    def __init__(self, provider_id, category_id, name, price, description=None, unit=None, duration_min=None):
        if not name:
            raise ValueError('Service must have a name')
        if price < 0:
            raise ValueError('Price must be non-negative')

        super().__init__()
        self.provider_id = provider_id
        self.category_id = category_id
        self.name = name
        self.price = price
        self.description = description
        self.unit = unit
        self.duration_min = duration_min

    def to_dict(self):
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'unit': self.unit,
            'duration_min': self.duration_min,
            'available': self.available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
