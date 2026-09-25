from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from src.core.database.connection import Base


class ProjectAttachment(Base):
    """Модель вложений к проекту."""
    
    __tablename__ = "project_attachment"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("project.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Основная информация о файле
    original_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Исходное имя файла")
    stored_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="Уникальное имя в хранилище")
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="Размер файла в байтах")
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False, comment="MIME-тип файла")
    
    # Дополнительные данные в JSONB
    file_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    
    # Временные метки
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # Связь с проектом
    project = relationship("Project", back_populates="attachments")