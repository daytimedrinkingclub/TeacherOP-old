# app/models/student_models.py
from ..extensions import db
from datetime import datetime
import uuid

# the user model where we will store the user data
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    firebase_uid = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=True)
    profile_image = db.Column(db.String(3000), unique=False, nullable=True)
    sign_in_provider = db.Column(db.String(100), unique=False, nullable=False, default="email")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    deleted_at = db.Column(db.DateTime, unique=False, nullable=True)

    courses = db.relationship('Course', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.id}>'

# the table that will store plan configurations
class Plan(db.Model):
    __tablename__ = "plans"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(5), nullable=False, default='INR')
    description = db.Column(db.Text, nullable=True)
    period = db.Column(db.Integer, nullable=False, default=30)
    active_courses = db.Column(db.Integer, nullable=False, default=1)
    assesments = db.Column(db.Integer, nullable=False, default=1)
    archived_courses = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Plan {self.id}>'

# This table will store the mapping of Users and Plans
class StudentPlan(db.Model):
    __tablename__ = "student_plans"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    plan_id = db.Column(db.String(36), db.ForeignKey('plans.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<StudentPlan {self.id}>'