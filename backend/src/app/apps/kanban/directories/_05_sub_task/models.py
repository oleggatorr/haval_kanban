# src\app\kanban\_05_sub_task\models.py

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

class Sub_Task(Base):
    __tablename__ = "sub_task"

    id = Column(Integer, primary_key=True, index=True)
    tasks_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=True)
    order_id = Column(Integer, nullable=True)

    task = relationship("Task", back_populates="sub_tasks")