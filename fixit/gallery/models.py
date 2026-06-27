from database import db
from fixit.base_model import BaseModel

class Gallery(BaseModel):
    __tablename__ = 'gallery'

    provider_id = db.Column(db.String(36), db.ForeignKey('providers.id'), nullable=False)
    service_id = db.Column(db.String(36), db.ForeignKey('services.id'), nullable=True)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(200), nullable=True)

    def __init__(self, provider_id, image_url, service_id=None, caption=None):
        if not image_url:
            raise ValueError('Gallery item must have an image URL')

        super().__init__()
        self.provider_id = provider_id
        self.image_url = image_url
        self.service_id = service_id
        self.caption = caption

    def to_dict(self):
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'service_id': self.service_id,
            'image_url': self.image_url,
            'caption': self.caption,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
