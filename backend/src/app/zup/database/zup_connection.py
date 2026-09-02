# src/core/database/connection.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from ..config.config import config
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Асинхронный SQLAlchemy Engine и Session (основной способ работы)
# -----------------------------------------------------------------------------

ASYNC_PG_URL = (
    f"postgresql+asyncpg://{config.USER_DB_USER}:"
    f"{quote_plus(config.USER_DB_PASSWORD)}@"
    f"{config.USER_DB_HOST}:"
    f"{config.USER_DB_PORT}/"
    f"{config.USER_DB_NAME}"
)

async_engine = create_async_engine(
    ASYNC_PG_URL,
    future=True,
    pool_size=config.DB_POOL_SIZE,
    max_overflow=config.DB_MAX_OVERFLOW,
    pool_timeout=config.DB_POOL_TIMEOUT,
    pool_recycle=config.POOL_RECYCLE,
    pool_pre_ping=True,
    connect_args={
        "timeout": 10, 
        "command_timeout": 10,
        "ssl": "prefer"  # или "require"
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

Base = declarative_base()


# -----------------------------------------------------------------------------
# Вспомогательные функции
# -----------------------------------------------------------------------------

async def get_db():
    """
    Асинхронный генератор зависимости для получения сессии БД.
    Используйте в FastAPI: Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_db_health() -> bool:
    """
    Проверка здоровья БД.
    Returns:
        bool: True если соединение успешно, False в противном случае
    """
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка проверки здоровья БД: {e}")
        return False


async def execute_raw_query(query: str, params: dict = None):
    """
    Выполнение сырого SQL запроса.
    
    Args:
        query: SQL запрос
        params: Параметры запроса (словарь)
    
    Returns:
        Результат выполнения запроса
    """
    try:
        async with async_engine.connect() as conn:
            if params:
                result = await conn.execute(text(query), params)
            else:
                result = await conn.execute(text(query))
            await conn.commit()
            return result
    except Exception as e:
        logger.error(f"❌ Ошибка выполнения запроса: {e}")
        raise


async def close_db_connections():
    """Закрытие всех соединений при завершении приложения."""
    try:
        await async_engine.dispose()
        logger.info("✅ Соединения с БД закрыты")
    except Exception as e:
        logger.error(f"❌ Ошибка при закрытии соединений: {e}")