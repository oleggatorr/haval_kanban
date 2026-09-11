from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TaskColumnBase(BaseModel):
    """Базовая схема колонки задач."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Название колонки")
    description: Optional[str] = Field(None, max_length=2000, description="Описание колонки")
    flags: Optional[List[Dict[str, Any]]] = Field(None, description="Дополнительные флаги/настройки в формате JSON")
    position: Optional[int] = Field(None, ge=0, description="Позиция колонки на доске (для сортировки)")


class TaskColumnCreate(TaskColumnBase):
    """Схема для создания колонки задач."""
    
    board_id: int = Field(..., gt=0, description="ID доски задач")


class TaskColumnUpdate(BaseModel):
    """Схема для частичного обновления колонки."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    flags: Optional[List[Dict[str, Any]]] = None
    position: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class TaskColumnResponse(TaskColumnBase):
    """Схема ответа для колонки задач."""
    
    id: int
    board_id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    remove_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskColumnListResponse(BaseModel):
    """Схема ответа для списка колонок."""
    
    items: list[TaskColumnResponse]
    total: int
    page: int
    page_size: int


class TaskColumnReorderRequest(BaseModel):
    """Схема для изменения порядка колонок."""
    
    column_ids: List[int] = Field(..., min_length=1, description="Список ID колонок в новом порядке")