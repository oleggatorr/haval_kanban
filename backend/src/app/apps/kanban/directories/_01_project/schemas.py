from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .._02_tab.schemas import Tab_deep_Response


# -----------------------------------------------------------------------------
# Базовые схемы
# -----------------------------------------------------------------------------

class ProjectBase(BaseModel):
    """Базовая схема проекта"""
    name: Optional[str] = Field(None, max_length=100, description="Название проекта")
    description: Optional[str] = Field(None, description="Описание проекта")
    updated_at: datetime = Field(None, description="Время последнего обновления")


class ProjectCreate(ProjectBase):
    """Схема для создания проекта"""
    pass


class ProjectUpdate(ProjectBase):
    """Схема для обновления проекта"""
    pass


class ProjectResponse(ProjectBase):
    """Схема ответа с данными проекта"""
    id: int
    
    class Config:
        from_attributes = True  # Для конвертации из SQLAlchemy модели
        
class Project_deep_Response(ProjectBase):
    """Схема ответа с данными проекта"""
    id: int
    tabs: List[Tab_deep_Response] = []
    
    class Config:
        from_attributes = True  # Для конвертации из SQLAlchemy модели