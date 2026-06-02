import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database: use /app/data for persistent storage in Docker
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # Use /app/data in Docker, or local data/ folder for development
        data_dir = os.environ.get('DATA_DIR') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{data_dir}/recipes.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads: use /app/uploads for persistent storage in Docker
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'uploads'
    )
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'json', 'csv'}
