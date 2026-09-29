from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TaskDataBase(BaseModel):
    """Базовая схема данных задачи."""
    owner_id: str = Field(..., min_length=1, max_length=10, description="ID владельца (employee_id)")
    big_description: Optional[str] = Field(None, description="Подробное описание")


class TaskDataCreate(TaskDataBase):
    pass


class TaskDataUpdate(BaseModel):
    owner_id: Optional[str] = Field(None, min_length=1, max_length=10)
    big_description: Optional[str] = None


class TaskDataResponse(TaskDataBase):
    id: int
    task_id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class TaskUserCreate(BaseModel):
    """Схема для добавления пользователя к задаче."""
    user_id: int = Field(..., gt=0)
    role: Optional[str] = None


class TaskUserResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    role: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """Базовая схема задачи."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    position: Optional[int] = Field(None, ge=0)
    
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    planing_date_time_start: Optional[datetime] = None
    planing_date_time_end: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Схема создания задачи."""
    column_id: int = Field(..., gt=0)
    status_id: Optional[int] = None
    
    data: Optional[TaskDataCreate] = None
    users: Optional[List[TaskUserCreate]] = []


class TaskUpdate(BaseModel):
    """Схема обновления задачи."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    position: Optional[int] = Field(None, ge=0)
    column_id: Optional[int] = Field(None, gt=0)
    status_id: Optional[int] = None
    
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    planing_date_time_start: Optional[datetime] = None
    planing_date_time_end: Optional[datetime] = None
    is_active: Optional[bool] = None
    
    data: Optional[TaskDataUpdate] = None


class TaskResponse(TaskBase):
    """Ответ API."""
    id: int
    column_id: int
    status_id: Optional[int] = None
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    
    data: Optional[TaskDataResponse] = None
    users: List[TaskUserResponse] = []
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int


class TaskReorderRequest(BaseModel):
    task_ids: List[int] = Field(..., min_length=1)