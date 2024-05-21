from database import db
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False,unique=True)
    email = db.Column(db.String(80),nullable=False)
    created_at = db.Column(DATETIME, nullable=False, default=func.now())
    meals = db.relationship("Meal", backref="user", order_by="Meal.id")