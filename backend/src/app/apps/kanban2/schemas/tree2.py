from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Вспомогательные схемы ---

class UserSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class SubtaskTree(BaseModel):
    id: int
    parent_task_id: int
    name: str
    description: Optional[str] = None
    status_id: Optional[int] = None
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    users: List[UserSimple] = []

    class Config:
        from_attributes = True

class TaskFlat(BaseModel):
    """Плоская структура задачи для фронтенда"""
    id: int
    column_id: int  # Важно для привязки к колонке на фронте
    name: str
    description: Optional[str] = None
    position: int
    status_id: Optional[int] = None
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    planing_date_time_start: Optional[datetime] = None
    planing_date_time_end: Optional[datetime] = None
    data: Optional[dict] = None
    users: List[UserSimple] = []
    
    # Агрегация для прогресс-бара
    subtasks_count: int = 0
    completed_subtasks_count: int = 0

    class Config:
        from_attributes = True

class ColumnFlat(BaseModel):
    """Плоская структура колонки"""
    id: int
    board_id: int
    name: str
    description: Optional[str] = None
    position: int
    flags: list = []

    class Config:
        from_attributes = True

class BoardFlat(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    last_activity_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Итоговый ответ API ---

class KanbanBoardResponse(BaseModel):
    """
    Оптимизированный ответ для Kanban-доски.
    Содержит отдельные списки для легкого маппинга на Vue 3.
    """
    board: BoardFlat
    columns: List[ColumnFlat]
    tasks: List[TaskFlat]
    subtasks: List[SubtaskTree]