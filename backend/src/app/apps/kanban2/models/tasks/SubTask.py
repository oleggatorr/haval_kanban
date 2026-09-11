from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class SubTask(Base):
    """Модель подзадачи."""
    
    __tablename__ = "sab_task"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent_task_id: Mapped[int] = mapped_column(Integer, ForeignKey("task.id"), nullable=False)
    status_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("task_status.id"), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # Изменено на Integer    name: Mapped[str] = mapped_column(String, nullable=False)
    date_time_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    date_time_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    planing_date_time_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    planing_date_time_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Связи
    parent_task = relationship("Task", back_populates="sub_tasks")
    status = relationship("TaskStatus", back_populates="sub_tasks")
    users = relationship("SubTaskUser", back_populates="sub_task", cascade="all, delete-orphan")