# src\app\knowledge_base\models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.core.database.connection import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # Механический цех, Сборочный и т.д.
    

    def __repr__(self):
        return f"<Department {self.name}>"
