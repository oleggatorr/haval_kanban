from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskBoardBase(BaseModel):
    """Базовая схема доски задач."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Название доски")
    description: Optional[str] = Field(None, max_length=2000, description="Описание доски")


class TaskBoardCreate(TaskBoardBase):
    """Схема для создания доски задач."""
    
    project_id: int = Field(..., gt=0, description="ID проекта")


class TaskBoardUpdate(BaseModel):
    """Схема для частичного обновления доски задач."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    is_active: Optional[bool] = None


class TaskBoardResponse(TaskBoardBase):
    """Схема ответа для доски задач."""
    
    id: int
    project_id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    remove_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskBoardListResponse(BaseModel):
    """Схема ответа для списка досок."""
    
    items: list[TaskBoardResponse]
    total: int
    page: int
    page_size: int