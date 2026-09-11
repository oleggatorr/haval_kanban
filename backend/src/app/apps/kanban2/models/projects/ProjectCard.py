from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import String, Boolean, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.connection import Base


class ProjectCard(Base):
    """Модель карточки в колонке проекта."""
    
    __tablename__ = "project_card"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    column_id: Mapped[int] = mapped_column(Integer, ForeignKey("project_column.id"), nullable=False)
    project_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("project.id"), nullable=True)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # Изменено на Integer    name: Mapped[str] = mapped_column(String, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    remove_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    
    # Связи
    column = relationship("ProjectColumn", back_populates="cards")
    project = relationship("Project", back_populates="cards")