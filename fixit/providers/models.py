from database import db
from fixit.base_model import BaseModel

class Provider(BaseModel):
    __tablename__ = 'providers'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    avg_rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    price_min = db.Column(db.Float, nullable=True)
    price_max = db.Column(db.Float, nullable=True)
    service_zone = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    user = db.relationship('User', backref=db.backref('provider_profile', uselist=False))
    services = db.relationship('Service', backref='provider', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='provider', lazy=True, cascade='all, delete-orphan')
    gallery = db.relationship('Gallery', backref='provider', lazy=True, cascade='all, delete-orphan')

    def __init__(self, user_id, bio=None, experience_years=None, price_min=None, price_max=None, service_zone=None, latitude=None, longitude=None):
        if price_min is not None and price_min < 0:
            raise ValueError('Price min must be non-negative')
        if price_max is not None and price_max < 0:
            raise ValueError('Price max must be non-negative')
        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValueError('Price min cannot be greater than price max')

        super().__init__()
        self.user_id = user_id
        self.bio = bio
        self.experience_years = experience_years
        self.price_min = price_min
        self.price_max = price_max
        self.service_zone = service_zone
        self.latitude = latitude
        self.longitude = longitude

    def update_rating(self):
        from fixit.reviews.models import Review
        reviews = Review.query.filter_by(provider_id=self.id).all()
        if reviews:
            self.avg_rating = sum(r.rating for r in reviews) / len(reviews)
            self.review_count = len(reviews)
        else:
            self.avg_rating = 0.0
            self.review_count = 0
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bio': self.bio,
            'experience_years': self.experience_years,
            'verified': self.verified,
            'avg_rating': self.avg_rating,
            'review_count': self.review_count,
            'price_min': self.price_min,
            'price_max': self.price_max,
            'service_zone': self.service_zone,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
