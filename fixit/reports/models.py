from database import db
from fixit.base_model import BaseModel

VALID_TARGET_TYPES = ['provider', 'review']

class Report(BaseModel):
    __tablename__ = 'reports'

    reporter_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.String(36), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    resolved = db.Column(db.Boolean, default=False)

    reporter = db.relationship('User', backref=db.backref('reports', lazy=True))

    def __init__(self, reporter_id, target_id, target_type, reason):
        if target_type not in VALID_TARGET_TYPES:
            raise ValueError('target_type must be provider or review')
        if not reason:
            raise ValueError('Report must have a reason')

        super().__init__()
        self.reporter_id = reporter_id
        self.target_id = target_id
        self.target_type = target_type
        self.reason = reason

    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'target_id': self.target_id,
            'target_type': self.target_type,
            'reason': self.reason,
            'resolved': self.resolved,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
