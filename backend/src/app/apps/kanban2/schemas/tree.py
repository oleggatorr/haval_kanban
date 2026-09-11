from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# --- Базовые компоненты дерева ---

class TaskDataTree(BaseModel):
    owner_id: str
    big_description: Optional[str] = None
    class Config: from_attributes = True

class TaskUserTree(BaseModel):
    user_id: int
    role: Optional[str] = None
    class Config: from_attributes = True

class TaskTree(BaseModel):
    """Задача внутри дерева."""
    id: int
    name: str
    description: Optional[str] = None
    position: Optional[int] = None
    status_id: Optional[int] = None
    
    # Даты
    date_time_start: Optional[datetime] = None
    date_time_end: Optional[datetime] = None
    
    data: Optional[TaskDataTree] = None
    users: List[TaskUserTree] = []
    
    class Config: from_attributes = True


class ColumnTree(BaseModel):
    """Колонка внутри дерева."""
    id: int
    name: str
    description: Optional[str] = None
    position: Optional[int] = None
    flags: Optional[List[dict]] = None
    
    tasks: List[TaskTree] = []
    
    class Config: from_attributes = True


class BoardTree(BaseModel):
    """Доска внутри дерева."""
    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    last_activity_at: Optional[datetime] = None
    
    columns: List[ColumnTree] = []
    
    class Config: from_attributes = True


class ProjectTreeResponse(BaseModel):
    """Корневой элемент дерева — Проект."""
    id: int
    name: str
    create_at: datetime
    is_active: bool
    
    board: Optional[BoardTree] = None
    
    class Config: from_attributes = True