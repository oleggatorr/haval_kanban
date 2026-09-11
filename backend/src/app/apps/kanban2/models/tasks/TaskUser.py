from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class TaskUser(Base):
    """Модель исполнителей/участников задачи."""
    
    __tablename__ = "task_users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("task.id"), nullable=False)
    employee_id: Mapped[str] = mapped_column(String(10), ForeignKey("user_role.employee_id"), nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Связи
    task = relationship("Task", back_populates="users")
    user = relationship("UserRole", backref="assigned_tasks")