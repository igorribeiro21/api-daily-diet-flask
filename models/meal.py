from database import db
from sqlalchemy.dialects.mysql import DATETIME, BOOLEAN
from sqlalchemy.sql import func

class Meal(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80),nullable=False)
    created_at = db.Column(DATETIME, nullable=False, default=func.now())
    inside_diet = db.Column(BOOLEAN, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    