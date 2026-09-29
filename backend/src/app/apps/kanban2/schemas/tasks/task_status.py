from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatusBase(BaseModel):
    """Базовая схема статуса задачи."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Название статуса")
    description: Optional[str] = Field(None, max_length=1000, description="Описание статуса")
    is_default: bool = Field(False, description="Является ли статусом по умолчанию")
    is_final: bool = Field(False, description="Является ли финальным статусом")
    is_active: bool = Field(True, description="Активен ли статус")


class TaskStatusCreate(TaskStatusBase):
    """Схема для создания статуса задачи."""
    pass


class TaskStatusUpdate(BaseModel):
    """Схема для обновления статуса задачи."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Название статуса")
    description: Optional[str] = Field(None, max_length=1000, description="Описание статуса")
    is_default: Optional[bool] = Field(None, description="Является ли статусом по умолчанию")
    is_final: Optional[bool] = Field(None, description="Является ли финальным статусом")
    is_active: Optional[bool] = Field(None, description="Активен ли статус")


class TaskStatusResponse(TaskStatusBase):
    """Схема ответа со статусом задачи."""
    
    id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    remove_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskStatusListResponse(BaseModel):
    """Схема ответа со списком статусов задач."""
    
    items: list[TaskStatusResponse]
    total: int


class TaskStatusSimpleResponse(BaseModel):
    """Упрощённая схема статуса для списков."""
    
    id: int
    name: str
    description: Optional[str] = None
    is_default: bool
    is_final: bool
    
    class Config:
        from_attributes = True


class TaskStatusListResponse(BaseModel):
    """Схема ответа со списком статусов задач."""
    
    items: list[TaskStatusResponse]
    total: int


class TaskStatusAllResponse(BaseModel):
    """Схема ответа со всеми статусами (без пагинации)."""
    
    items: list[TaskStatusSimpleResponse]
    total: int