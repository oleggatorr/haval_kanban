from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database.connection import Base

# Импортируем модель профиля пользователя для типизации связей
# Убедитесь, что путь правильный относительно структуры вашего проекта
from src.app.apps.kanban.user_profille.profille.profille_models import UserProfile 


# -----------------------------------------------------------------------------
# Промежуточные таблицы (Many-to-Many)
# -----------------------------------------------------------------------------

class TaskAssignee(Base):
    """
    Промежуточная таблица для связи задач и исполнителей.
    Позволяет назначать нескольких пользователей на одну задачу.
    """
    __tablename__ = "task_assignees"

    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), primary_key=True)
    employee_id = Column(String(20), ForeignKey("user_profiles.employee_id", ondelete="CASCADE"), primary_key=True)

    # Отношения для удобства навигации (опционально, но полезно)
    task = relationship("Task", back_populates="assignees")
    user_profile = relationship("UserProfile", back_populates="assigned_tasks")


# -----------------------------------------------------------------------------
# Основные модели
# -----------------------------------------------------------------------------

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    column_id = Column(Integer, ForeignKey("column.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=True)

    order_id = Column(Integer, nullable=True)
    is_complit = Column(Boolean, nullable=True, default=False)

    # Связи
    column = relationship("Column", back_populates="tasks")
    sub_tasks = relationship("Sub_Task", back_populates="task", cascade="all, delete-orphan")
    
    # Новая связь: Исполнители задачи
    assignees = relationship("TaskAssignee", back_populates="task", cascade="all, delete-orphan")