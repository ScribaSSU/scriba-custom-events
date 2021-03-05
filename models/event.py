from datetime import datetime
from models.db import db


class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    repeat = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Event {self.event_id}>"

    @staticmethod
    def find_all():
        return db.session.query(Event).all()
