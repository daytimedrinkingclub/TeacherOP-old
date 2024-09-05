# app/models/content_models.py
from ..extensions import db
from datetime import datetime
import uuid

# This table will store the content related to the course, checkpoint and question
class Content(db.Model):
    __tablename__ = "contents"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    checkpoint_id = db.Column(db.String(36), db.ForeignKey('checkpoints.id'), nullable=False)
    question_id = db.Column(db.String(36), db.ForeignKey('questions.id'), nullable=False)
    content_type = db.Column(db.String(36), nullable=False)
    content_json = db.Column(db.JSON, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
