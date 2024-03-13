from datetime import datetime
from flaskWeb import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    sex = db.Column(db.String(10))
    activity_level = db.Column(db.String(50))
    current_weight = db.Column(db.Float)
    goal_weight = db.Column(db.Float)
    protein_macros = db.Column(db.Float, nullable=True)
    fat_macros = db.Column(db.Float, nullable=True)
    carb_macros = db.Column(db.Float, nullable=True)
    weeks_to_goal = db.Column(db.Integer, nullable=True)
    new_calorie_goal = db.Column(db.Float, nullable=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



        