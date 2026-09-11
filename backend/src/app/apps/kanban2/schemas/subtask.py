from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SubTaskUserCreate(BaseModel):
    """Схема добавления пользователя к подзадаче."""
    user_id: int = Field(..., gt=0)
    role: Optional[str] = None


class SubTaskUserResponse(BaseModel):
    id: int
    sub_task_id: int
    user_id: int
    role: Optional[str] = None
    
    class Config:
        from_attributes = True


class SubTaskBase(BaseModel):
    """Базовая схема подзадачи."""
    name: str = Field(..., min_length=1, max_length=255, description="Название подзадачи")
    description: Optional[str] = Field(None, max_length=2000, description="Описание")
    position: Optional[int] = Field(None, ge=0, description="Позиция в списке подзадач")
    
    # Даты
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    planing_date_time_start: Optional[datetime] = None
    planing_date_time_end: Optional[datetime] = None


class SubTaskCreate(SubTaskBase):
    """Схема создания подзадачи."""
    parent_task_id: int = Field(..., gt=0, description="ID родительской задачи")
    status_id: Optional[int] = Field(None, description="ID статуса")
    users: Optional[List[SubTaskUserCreate]] = []


class SubTaskUpdate(BaseModel):
    """Схема обновления подзадачи."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    position: Optional[int] = Field(None, ge=0)
    status_id: Optional[int] = None
    
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    planing_date_time_start: Optional[datetime] = None
    planing_date_time_end: Optional[datetime] = None
    is_active: Optional[bool] = None


class SubTaskResponse(SubTaskBase):
    """Ответ API."""
    id: int
    parent_task_id: int
    status_id: Optional[int] = None
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    
    users: List[SubTaskUserResponse] = []
    
    class Config:
        from_attributes = True


class SubTaskListResponse(BaseModel):
    items: list[SubTaskResponse]
    total: int


class SubTaskReorderRequest(BaseModel):
    """Для drag & drop подзадач внутри одной задачи."""
    subtask_ids: List[int] = Field(..., min_length=1)