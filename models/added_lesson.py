from datetime import datetime
from models.db import db

class AddedLesson(db.Model):
    __tablename__ = "addedLesson"
    lesson_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    lesson_name = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    group = db.Column(db.String(200), nullable=False)
    week_day = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String(200), nullable=False)
    subgroup = db.Column(db.String(200), nullable=False)

    #числитель/знаменатель
    week_type = db.Column(db.String(200), nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)

    #лекция/практика
    lesson_type = db.Column(db.String(200), nullable=False)
    teacher_name = db.Column(db.String(200), nullable=False)

    time_begin = db.Column(db.Time, nullable=False)
    time_end = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"<Lesson {self.lesson_id}>"

    @staticmethod
    def find_all():
        return db.session.query(AddedLesson).all()

    @staticmethod
    def find_added_lessons(user_id=2):
        return db.session.query(AddedLesson).filter_by(user_id=user_id).all()

    @staticmethod
    def delete_lesson(lesson_id=2):
        db.session.query(AddedLesson).filter_by(lesson_id=lesson_id).delete()
        db.session.commit()

    @staticmethod
    def save_lesson(user_id, lesson_name, place, department, group, subgroup, week_day, week_type,
                   lesson_number, lesson_type, teacher_name, time_begin, time_end):
        new_lesson = AddedLesson(
            user_id=user_id,
            lesson_name=lesson_name,
            department=department,
            group=group,
            week_day=week_day,
            week_type=week_type,
            lesson_number=lesson_number,
            lesson_type=lesson_type,
            teacher_name=teacher_name,
            time_begin=time_begin,
            time_end=time_end,
            subgroup=subgroup,
            place=place
        )
        db.session.add(new_lesson)
        db.session.commit()
        return new_lesson.lesson_id