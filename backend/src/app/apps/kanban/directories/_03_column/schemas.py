from pydantic import BaseModel, Field
from typing import Optional, List
from .._04_task.schemas import Task_deep_Response

# -----------------------------------------------------------------------------
# Базовые схемы
# -----------------------------------------------------------------------------

class ColumnBase(BaseModel):
    """Базовая схема колонки"""
    name: Optional[str] = Field(None, max_length=100, description="Название колонки")
    order_id: Optional[int] = Field(None, description="Порядковый номер колонки")
    is_start: bool = Field(False, description="Является ли колонка начальной")
    is_final: bool = Field(False, description="Является ли колонка финальной")
    is_active: bool = Field(True, description="Активна ли колонка")


class ColumnCreate(ColumnBase):
    """Схема для создания колонки"""
    tab_id: int = Field(..., description="ID таба, к которому принадлежит колонка")


class ColumnUpdate(ColumnBase):
    """Схема для обновления колонки"""
    pass


class ColumnResponse(ColumnBase):
    """Схема ответа с данными колонки"""
    id: int
    tab_id: int
    
    class Config:
        from_attributes = True  # Для конвертации из SQLAlchemy модели

class Column_deep_Response(ColumnBase):
    """Схема глубокого ответа с данными колонки"""
    id: int
    tab_id: int
    tasks: List[Task_deep_Response] = []
    class Config:
        from_attributes = True  # Для конвертации из SQLAlchemy модели


class ReorderColumnsRequest(BaseModel):
    """Схема запроса для изменения порядка колонок"""
    column_ids: List[int] = Field(..., description="Список ID колонок в новом порядке")