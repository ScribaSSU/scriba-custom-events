from datetime import datetime
from models.db import db


class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date_begin = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_end = db.Column(db.DateTime, default=date_begin)
    type = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Event {self.event_id}>"

    @staticmethod
    def find_all():
        return db.session.query(Event).all()

    @staticmethod
    def save_event(user_id, event_name, date_begin, date_end, type, description=''):
        new_event = Event(
            user_id=user_id,
            event_name=event_name,
            description=description,
            date_begin=date_begin,
            date_end=date_end,
            type=type)

        db.session.add(new_event)
        db.session.commit()
        return new_event.id
