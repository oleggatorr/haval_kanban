from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from src.core.database.connection import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    # === Идентификация ===
    employee_id = Column(
        String(20), 
        ForeignKey("auth_users.employee_id", ondelete="CASCADE"),
        primary_key=True, 
        unique=True, 
        index=True
    )
    
    # === Отображение ===
    display_name = Column(String(150), nullable=False, comment="Имя для отображения")
    avatar_url = Column(String(500), nullable=True, comment="Ссылка на аватар")
    
    # === Права доступа (RBAC) ===
    # Структура: {"system": {...}, "projects": [...]}
    permissions = Column(
        JSONB, 
        nullable=False, 
        server_default='{"system": {"role": "user", "global_flags": []}, "projects": []}', 
        comment="Системные роли и проектные доступы"
    )
    
    # === Настройки аккаунта (UI/UX) ===
    preferences = Column(
        JSONB, 
        nullable=False, 
        server_default='{}', 
        comment="Настройки интерфейса и уведомлений"
    )
    
    # === Статус ===
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # === Аудит ===
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # === Связи ===
    auth_user = relationship("AuthUser", back_populates="profile", uselist=False)
    assigned_tasks = relationship("TaskAssignee", back_populates="user_profile")