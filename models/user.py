from database import db
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')
    created_at = db.Column(DATETIME, nullable=False, default=func.now())
    meals = db.relationship("Meal", backref="user", order_by="Meal.id")