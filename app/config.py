import os
from dotenv import load_dotenv

# Load environment variables from .env.local
print(f"Current working directory: {os.getcwd()}")  # Debug print
env_path = os.path.join(os.getcwd(), '.env.local')
print(f".env.local path: {env_path}")  # Debug print
print(f".env.local exists: {os.path.exists(env_path)}")  # Debug print

load_dotenv(env_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    print(f"Database URL from env: {os.getenv('DATABASE_URL')}")  # Debug print
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    print(f"Final Database URL: {SQLALCHEMY_DATABASE_URI}")  # Debug print
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}