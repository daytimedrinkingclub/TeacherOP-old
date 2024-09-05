import os
import logging
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    logging.info(f"initializing firebase")
    # Check if running in a production environment (e.g., Heroku)
    if os.environ.get('FLASK_ENV') == 'production':
        logging.info(f"initializing firebase in production")
        # Load credentials from individual environment variables
        cred_dict = {
            "type": os.environ.get('FIREBASE_TYPE'),
            "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
            "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
            "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
            "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_CERT_URL'),
            "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
        }
        cred = credentials.Certificate(cred_dict)
    else:
        logging.info(f"initializing firebase in development")
        # Load credentials from a file in development
        file_path = os.path.join(os.path.dirname(__file__), "Key.json")
        cred = credentials.Certificate(file_path)
    
    logging.info(f"firebase initialized")
    firebase_admin.initialize_app(cred)