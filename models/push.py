from datetime import datetime
import uuid
from . import db
from .abc import BaseModel


class PushManager(db.Model, BaseModel):

    __tablename__ = 'push_manager'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36))
    android_key = db.Column(db.String(256), unique=True)
    app_name = db.Column(db.String(100))
    sns_arn = db.Column(db.String(512))
    push = db.relationship('Push')
    installation = db.relationship('Installation')

    to_json_filter = ['id']

    def __init__(self, android_key, app_name, sns_arn):
        self.android_key = android_key
        self.app_name = app_name
        self.sns_arn = sns_arn
        self.uuid = str(uuid.uuid4())

class Push(db.Model, BaseModel):

    __tablename__ = 'push'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    manager_id = db.Column(db.Integer, db.ForeignKey("push_manager.id"), nullable=False)
    pmanager = db.relationship('PushManager', back_populates="push")

    def __init__(self, message, id_manager):
        self.message = message
        self.id_manager = id_manager
