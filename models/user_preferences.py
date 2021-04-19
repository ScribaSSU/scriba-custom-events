from models.db import db


class UserPreferences(db.Model):
    __tablename__ = "preferences"
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_department = db.Column(db.String(200), nullable=False)
    user_course = db.Column(db.String(200), nullable=False)
    user_group = db.Column(db.String(200), nullable=False)
    show_hidden = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Факультет {self.user_department}, группа {self.user_group}>"

    @staticmethod
    def find_all():
        return db.session.query(UserPreferences).all()

    @staticmethod
    def get_user_preferences(user_id=2):
        return db.session.query(UserPreferences).filter_by(user_id=user_id).first()

    @staticmethod
    def update_show_preferences(user_id=2):
        user = db.session.query(UserPreferences).filter_by(user_id=user_id).first()
        if user:
            user.show_hidden = not user.show_hidden
            db.session.commit()

    @staticmethod
    def save_user_preferences(user_id, user_department, user_course, user_group, show_hidden=False):
        new_preference = UserPreferences(
            user_id=user_id,
            user_department=user_department,
            user_course=user_course,
            user_group=user_group,
            show_hidden=show_hidden)
        db.session.merge(new_preference)
        db.session.commit()
