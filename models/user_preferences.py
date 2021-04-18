from models.db import db


class UserPreferences(db.Model):
    __tablename__ = "preferences"
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_department = db.Column(db.String(200))
    user_course = db.Column(db.String(200))
    user_group = db.Column(db.String(200))

    def __repr__(self):
        return f"<Факультет {self.user_department}, группа {self.user_group}>"

    @staticmethod
    def find_all():
        return db.session.query(UserPreferences).all()

    @staticmethod
    def get_user_group(vk_id=2):
        return db.session.query(UserPreferences).filter_by(user_id=vk_id).all()

    @staticmethod
    def save_user_group(user_id, user_department, user_course, user_group):
        new_preference = UserPreferences(
            user_id=user_id,
            user_department=user_department,
            user_course=user_course,
            user_group=user_group)
        db.session.merge(new_preference)
        db.session.commit()