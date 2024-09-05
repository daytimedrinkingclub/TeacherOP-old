# app/utils/jwt_util.py
import logging
from datetime import datetime, timedelta
import jwt
from flask import current_app


class JWTUtil:
    @staticmethod
    def generate_jwt_token(student_id):
        logging.info(f"generating jwt for middelware for student_id: {student_id}")
        payload = {
            'student_id': student_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    @staticmethod
    def decode_jwt_token(token):
        logging.info(f"decoding jwt for internal auth")
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['student_id']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
    @staticmethod
    def decode_firebase_token(token):
        logging.info(f"decoding firebase token for auth in util")
        from firebase_admin import auth
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token  # Return the entire decoded token payload
        except auth.ExpiredIdTokenError:
            return {'error': 'Token expired. Please log in again.'}
        except auth.InvalidIdTokenError:
            return {'error': 'Invalid token. Please log in again.'}
