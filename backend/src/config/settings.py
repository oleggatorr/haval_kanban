import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Settings:
    """Класс для хранения настроек приложения"""

    HOST = os.getenv('HOST', 'localhost')
    # Static CSRF Token
    CSRF_TOKEN = os.getenv('CSRF_TOKEN', 'default_csrf_token_123')
    CSRF_TOKEN_ENABLED = os.getenv('CSRF_TOKEN_ENABLED', 'true').lower() == 'true'
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Connection Pool
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 10))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', 20))
    DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', 30))
    POOL_RECYCLE = int(os.getenv('POOL_RECYCLE', 3600))

    # Database
    DB_HOST         = str(os.getenv('DB_HOST', "localhost"))
    DB_PORT         = int(os.getenv('DB_PORT', 5432))
    DB_USER         = str(os.getenv('DB_USER', "postgres"))
    DB_PASSWORD     = str(os.getenv('DB_PASSWORD'))
    DB_NAME         = str(os.getenv('DB_NAME',"base_hesk"))

    SECRET_KEY      = str(os.getenv('SECRET_KEY',"your-secret-key-change-this-in-production"))
    
    
    # DB users
    USER_DB_HOST         = str(os.getenv('USER_DB_HOST'))
    USER_DB_PORT = int(os.getenv('USER_DB_PORT', '5432'))
    USER_DB_USER         = str(os.getenv('USER_DB_USER'))
    USER_DB_PASSWORD     = str(os.getenv('USER_DB_PASSWORD'))
    USER_DB_NAME         = str(os.getenv('USER_DB_NAME'))



settings = Settings()