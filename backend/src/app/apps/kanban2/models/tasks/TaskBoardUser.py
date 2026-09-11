from datetime import datetime, timezone
from typing import Optional, Dict, Any

from sqlalchemy import String, Boolean, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class TaskBoardUser(Base):
    """Модель пользователей доски задач и их прав."""
    
    __tablename__ = "task_board_users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("task_board.id"), nullable=False)
    employee_id: Mapped[str] = mapped_column(String(10), ForeignKey("user_role.employee_id"), nullable=False)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # Изменено на Integer    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Связи
    board = relationship("TaskBoard", back_populates="board_users")
    user = relationship("UserRole", backref="task_board_memberships")