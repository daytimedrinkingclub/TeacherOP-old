# app/models/question_models.py
from ..extensions import db
from datetime import datetime
import uuid

# This table will store the questions asked by the users
class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    checkpoint_id = db.Column(db.String(36), db.ForeignKey('checkpoints.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_format = db.Column(db.String(36), nullable=False)
    question_type = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    answers = db.relationship('Answer', backref='question', lazy=True)