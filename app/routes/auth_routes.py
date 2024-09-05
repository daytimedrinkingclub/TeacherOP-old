import logging
from datetime import datetime
from flask import jsonify, request
from . import auth_bp
from firebase_admin import auth
from ..services.data_service import DataService
from ..utils.jwt_util import JWTUtil

@auth_bp.route('/signup', methods=['POST'])
@auth_bp.route('/login', methods=['POST'])
def auth_handler():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the ID token and sign-in provider from the data
    id_token = data.get('token')
    sign_in_provider = data.get('provider', 'email')

    # Determine the action based on the request path ('signup' or 'login')
    action = request.path.split('/')[-1]

    # Log the authentication attempt with the token
    logging.debug(f"{action.capitalize()} attempt with token: {id_token}")

    try:
        # Verify the ID token using Firebase authentication
        decoded_token = auth.verify_id_token(id_token)
        # Extract the Firebase UID from the decoded token
        firebase_uid = decoded_token['uid']

        # Log the decoded token with the Firebase UID
        logging.debug(f"Decoded token for Firebase UID: {firebase_uid}")

        # Retrieve the student using the Firebase UID from the data service
        student = DataService.get_student_by_firebase_uid(firebase_uid)
        if student is None:
            if action == 'signup':
                # If the action is 'signup' and the student doesn't exist, create a new student
                email = decoded_token['email']
                name = decoded_token.get('name', '')
                profile_image = decoded_token.get('picture', '')

                # Prepare the student data for creation
                student_data = {
                    'firebase_uid': firebase_uid,
                    'email': email,
                    'name': name,
                    'profile_image': profile_image,
                    'sign_in_provider': sign_in_provider,
                }
                # Create a new student using the data service
                student = DataService.create_student(student_data)
            else:
                # If the action is 'login' and the student doesn't exist, return an error
                logging.warning(f"No student found with Firebase UID: {firebase_uid}")
                return jsonify(error='Student not found'), 404

        # Get the student ID
        student_id = student.id
        # Generate a JWT token using the student ID
        token = JWTUtil.generate_jwt_token(student_id)
        # Log the generated JWT token with the student ID
        logging.info(f"Generated JWT token for student ID: {student_id}")
        # Return the token with a success status code (200 for login, 201 for signup)
        return jsonify(token=token), 200 if action == 'login' else 201
    except auth.InvalidIdTokenError:
        # If the ID token is invalid, log an error and return an error response
        logging.error("Invalid ID token provided.")
        return jsonify(error='Invalid ID token'), 401
    except Exception as e:
        # If any other exception occurs, log the error and return an error response
        logging.error(f"Error during {action}: {str(e)}")
        return jsonify(error='An error occurred'), 500
