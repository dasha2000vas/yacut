from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
