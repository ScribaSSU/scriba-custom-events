from datetime import datetime
from models.db import db

class AddedLesson(db.Model):
    __tablename__ = "addedLesson"
    lesson_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(200), nullable=False)
    edu_form = db.Column(db.String(200), nullable=False)
    group_type = db.Column(db.String(200), nullable=False)
    group = db.Column(db.String(200), nullable=False)
    week_day = db.Column(db.String(200), nullable=False)
    week_type = db.Column(db.String(200), nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)
    lesson_type = db.Column(db.String(200), nullable=False)
    teacher_name = db.Column(db.String(200))  # имя преподавателя наверное можно занулять?
                                              # ну мало ли, пользователь не в курсе))0
    lesson_name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Lesson {self.event_id}>"

    @staticmethod
    def find_all():
        return db.session.query(AddedLesson).all()

def find_added_lessons(user_id=2):
    return db.session.query(AddedLesson).filter_by(user_id=user_id).all()
