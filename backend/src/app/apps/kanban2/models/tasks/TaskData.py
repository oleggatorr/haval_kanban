from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class TaskData(Base):
    """Модель дополнительных данных задачи (1 к 1)."""
    
    __tablename__ = "task_data"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("task.id"), unique=True, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(10), ForeignKey("user_role.employee_id"), nullable=False)
    big_description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Связи
    task = relationship("Task", back_populates="data")
    owner = relationship("UserRole", backref="owned_tasks_data")