import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    """Класс для хранения настроек приложения"""

    # Connection Pool
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 10))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', 20))
    DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', 30))
    POOL_RECYCLE = int(os.getenv('POOL_RECYCLE', 3600))
    
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


    # DB users
    USER_DB_HOST         = str(os.getenv('USER_DB_HOST'))
    USER_DB_PORT         = int(os.getenv('USER_DB_PORT'))
    USER_DB_USER         = str(os.getenv('USER_DB_USER'))
    USER_DB_PASSWORD     = str(os.getenv('USER_DB_PASSWORD'))
    USER_DB_NAME         = str(os.getenv('USER_DB_NAME'))

config = Config()