# src\app\kanban\_01_project\models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableDict

# from .._02_tab.models import Tab
from sqlalchemy.dialects.postgresql import JSON 

from src.core.database.connection import Base


# -----------------------------------------------------------------------------
# Основные модели
# -----------------------------------------------------------------------------

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tabs = relationship("Tab", back_populates="project", cascade="all, delete-orphan")
