from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
course_bp = Blueprint('course', __name__, url_prefix='/courses')

from . import auth_routes, course_routes