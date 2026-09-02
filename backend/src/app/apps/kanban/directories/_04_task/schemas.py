from pydantic import BaseModel, Field
from typing import Optional, List
from .._05_sub_task.schemas import SubTaskResponse


# Схема для отображения исполнителя (упрощенная)
class AssigneeInfo(BaseModel):
    employee_id: str
    display_name: str
    
    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """Базовая схема задачи"""
    name: Optional[str] = Field(None, max_length=100, description="Название задачи")
    order_id: Optional[int] = Field(None, description="Порядковый номер задачи")
    is_complit: bool = Field(False, description="Выполнена ли задача")


class TaskCreate(TaskBase):
    """Схема для создания задачи"""
    column_id: int = Field(..., description="ID колонки, к которой принадлежит задача")
    assignee_ids: Optional[List[str]] = Field(default_factory=list, description="Список employee_id исполнителей")


class TaskUpdate(TaskBase):
    """Схема для обновления задачи"""
    assignee_ids: Optional[List[str]] = None


class TaskResponse(TaskBase):
    """Схема ответа с данными задачи"""
    id: int
    column_id: int
    assignees: List[AssigneeInfo] = []  # Список текущих исполнителей
    
    class Config:
        from_attributes = True  
        
class Task_deep_Response(TaskResponse):
    """Схема ответа с данными задачи и подзадачами"""
    subtasks: List[SubTaskResponse] = []
    
    class Config:
        from_attributes = True  