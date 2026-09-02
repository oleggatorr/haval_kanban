# src\app\kanban\_03_column\models.py

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

class Column(Base):
    __tablename__ = "column"

    id = Column(Integer, primary_key=True, index=True)
    tab_id = Column(Integer, ForeignKey("tab.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=True)
    order_id = Column(Integer, nullable=True)

    is_start =  Column(Boolean, nullable=False, default= False)
    is_final =  Column(Boolean, nullable=False, default= False)
    is_active = Column(Boolean, nullable=False, default= True)


    tab = relationship("Tab", back_populates="colums")

    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan")