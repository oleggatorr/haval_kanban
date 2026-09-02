# src/app/user_auth/users/models.py
import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from src.core.database.connection import Base

class AuthUser(Base):
    __tablename__ = "auth_users"
    
    # Поля из внешней системы - делаем nullable для поддержки регистрации
    employee_id = Column(String(20), primary_key=True, unique=True, index=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    
    # Поля для локальной аутентификации
    login = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Связь с профилем пользователя (один-к-одному)
    profile = relationship(
        "UserProfile", 
        back_populates="auth_user",
        uselist=False,  # Указывает, что это один-к-одному
        cascade="all, delete-orphan"  # При удалении AuthUser удаляется и профиль
    )