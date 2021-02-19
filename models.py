from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base
from datetime import datetime


class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    event_name = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    repeat = Column(Boolean, default=False)

    def __init__(self,
                 user_id: int,
                 event_name: String,
                 description: String = None,
                 date: datetime = None,
                 repeat: bool = None):
        self.user_id = user_id
        self.event_name = event_name
        if description is not None:
            self.description = description
        if date is not None:
            self.date = date
        if repeat is not None:
            self.repeat = repeat

    def __repr__(self):
        return f'<Event {self.event_id}>'
