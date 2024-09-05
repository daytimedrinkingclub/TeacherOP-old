# socketio_config.py
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins=['http://localhost:3000', 'https://teacherop.com'])

def init_socketio(app):
    socketio.init_app(app)