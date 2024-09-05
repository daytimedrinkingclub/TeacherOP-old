import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .config import config
from .extensions import db, init_extensions
from .socketio_config import socketio, init_socketio
from . import firebase_config

def create_app(config_name=None):
    from dotenv import load_dotenv
    
    # Load environment variables from .env.local
    env_path = os.path.join(os.getcwd(), '.env.local')
    load_dotenv(env_path)
    
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    print(f"Config name: {config_name}")  # Debug print
    print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")  # Debug print
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")  # Debug print

    app.config.from_object(config[config_name])
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")  # Debug print
    
    # Initialize extensions
    init_extensions(app)  # Commented out
    
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://teacherop.com"]}})
    firebase_config.initialize_firebase()
    init_socketio(app)  # Initialize SocketIO

    with app.app_context():
        from .routes import auth_bp, course_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(course_bp)

        db.create_all()  # Commented out

    # Serve static files from the 'static' folder
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_static(path):
        if path.startswith("static/"):
            return send_from_directory(app.static_folder, path[7:])
        elif path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app