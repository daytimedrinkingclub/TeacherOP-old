# app/models/course_models.py
from ..extensions import db
from datetime import datetime
import uuid

# This table will store the queries made by the users
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    input_query = db.Column(db.Text, nullable=False)
    course_status = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    checkpoints = db.relationship('Checkpoint', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.id}>'

# This table will store the messages made by the users
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    message = db.Column(db.Text)
    role = db.Column(db.String(36))
    raw_message = db.Column(db.JSON)
    sequence_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)