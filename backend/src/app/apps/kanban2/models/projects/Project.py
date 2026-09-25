from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class Project(Base):
    """Модель проекта."""
    
    __tablename__ = "project"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Связи
    cards = relationship("ProjectCard", back_populates="project")
    data = relationship("ProjectData", back_populates="project", uselist=False)
    task_board = relationship("TaskBoard", back_populates="project", uselist=False)
    
    attachments = relationship("ProjectAttachment", back_populates="project", cascade="all, delete-orphan")