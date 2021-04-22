from datetime import datetime
from models.db import db


class HiddenLesson(db.Model):
    __tablename__ = "hiddenLesson"
    hidden_lesson_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(200), nullable=False)
    group = db.Column(db.String(200), nullable=False)
    sub_group = db.Column(db.String(200), nullable=False)
    week_day = db.Column(db.Integer, nullable=False)
    week_type = db.Column(db.String(200), nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<HiddenLesson {self.hidden_lesson_id}>"

    @staticmethod
    def find_all():
        return db.session.query(HiddenLesson).all()

    @staticmethod
    def find_hidden_lessons(user_id):
        return db.session.query(HiddenLesson).filter_by(user_id=user_id).all()

    @staticmethod
    def find_hidden_lessons_by_day(user_id, week_day):
        return db.session.query(HiddenLesson).filter_by(user_id=user_id, week_day=week_day).all()

    @staticmethod
    def hide_lesson(user_id, user_department, user_group, sub_group, week_day, week_type, lesson_number):
        new_hidden_lesson = HiddenLesson(
            user_id=user_id,
            department=user_department,
            group=user_group,
            sub_group=sub_group,
            week_day=week_day,
            week_type=week_type,
            lesson_number=lesson_number)
        db.session.add(new_hidden_lesson)
        db.session.commit()
        return new_hidden_lesson.hidden_lesson_id

    @staticmethod
    def unhide_lesson(lesson_id):
        db.session.query(HiddenLesson).filter_by(hidden_lesson_id=lesson_id).delete()
        db.session.commit()

    @staticmethod
    def clear_lessons(user_id):
        db.session.query(HiddenLesson).filter_by(user_id=user_id).delete()
        db.session.commit()