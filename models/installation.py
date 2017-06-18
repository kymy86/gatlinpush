import uuid
from datetime import datetime
from . import db
from .abc import BaseModel


class Installation(db.Model, BaseModel):

    __tablename__ = 'installation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.Integer, db.ForeignKey('push_manager.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    device_id = db.Column(db.String(64))
    uuid = db.Column(db.String(36))
    __table_args__ = (
        db.UniqueConstraint('app_id', 'device_id', name='_one_instal_ix'),
    )

    to_json_filter = ['id']

    def __init__(self, app_id, device_id):
        self.app_id = app_id
        self.device_id = device_id
        self.uuid = str(uuid.uuid4())
