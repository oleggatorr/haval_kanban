# src\app\kanban\_02_tab\models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database.connection import Base


# -----------------------------------------------------------------------------
# Промежуточные таблицы (Many-to-Many)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Основные модели
# -----------------------------------------------------------------------------

class Tab(Base):
    __tablename__ = "tab"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=True)
    order_id = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tabs")

    colums = relationship("Column", back_populates="tab", cascade="all, delete-orphan")

