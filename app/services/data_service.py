# app/services/data_service.py
import logging
from ..extensions import db
from ..models.student_models import Student


class DataService:
    @staticmethod
    def get_student_by_firebase_uid(firebase_uid):
        return Student.query.filter_by(firebase_uid=firebase_uid).first()

    @staticmethod
    def create_student(student_data):
        logging.info(f"dataservice called with user data: {student_data}")
        student = Student(
            firebase_uid=student_data['firebase_uid'],
            email=student_data['email'],
            name=student_data['name'],
            profile_image=student_data['profile_image'],
            sign_in_provider=student_data['sign_in_provider'],
        )
        db.session.add(student)
        db.session.commit()
        logging.info(f"New Student created: {student}")
        return student

    @staticmethod
    def get_student_by_id(student_id):
        student = Student.query.get(student_id)
        logging.info(f"Student retrieved by ID: {student}")
        return student

    @staticmethod
    def get_student_by_email(email):
        student = Student.query.filter_by(email=email).first()
        logging.info(f"Student retrieved by email: {student}")
        return student
    
    @staticmethod
    def get_student_courses(student_id):
        student = DataService.get_student_by_id(student_id)
        logging.info(f"Student courses: {student.courses}")
        return student.courses # to be modified later