from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import String, Boolean, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class ProjectColumn(Base):
    """Модель колонки доски проекта."""
    
    __tablename__ = "project_column"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("project_board.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # Изменено на Integer    name: Mapped[str] = mapped_column(String, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Связи
    board = relationship("ProjectBoard", back_populates="columns")
    cards = relationship("ProjectCard", back_populates="column", cascade="all, delete-orphan")