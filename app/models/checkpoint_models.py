# app/models/checkpoint_models.py
from ..extensions import db
from datetime import datetime
import uuid

# This table will store the checkpoints created for the course
class Checkpoint(db.Model):
    __tablename__ = "checkpoints"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    checkpoint_details = db.Column(db.Text, nullable=False)
    checkpoint_number = db.Column(db.Integer, nullable=False)
    checkpoint_status = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    questions = db.relationship('Question', backref='checkpoint', lazy=True)
    contents = db.relationship('Content', backref='checkpoint', lazy=True)