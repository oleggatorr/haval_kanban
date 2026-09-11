from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.connection import Base


class UserRole(Base):
    """Модель роли пользователя с глобальными правами доступа."""
    
    __tablename__ = "user_role"
    
    employee_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    global_permissions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)