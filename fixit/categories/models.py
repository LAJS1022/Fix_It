from database import db
from fixit.base_model import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(10), nullable=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=True)

    services = db.relationship('Service', backref='category', lazy=True)

    def __init__(self, name, slug, icon=None, description=None):
        if not name:
            raise ValueError('Category must have a name')
        if not slug:
            raise ValueError('Category must have a slug')

        super().__init__()
        self.name = name
        self.slug = slug
        self.icon = icon
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
