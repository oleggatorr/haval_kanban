from pydantic import BaseModel, Field
from typing import Optional, List

from .._03_column.schemas import Column_deep_Response

# -----------------------------------------------------------------------------
# Базовые схемы
# -----------------------------------------------------------------------------

class TabBase(BaseModel):
    """Базовая схема таба"""
    name: Optional[str] = Field(None, max_length=100, description="Название таба")
    order_id: Optional[int] = Field(None, description="Порядковый номер таба")


class TabCreate(TabBase):
    """Схема для создания таба"""
    project_id: int = Field(..., description="ID проекта, к которому принадлежит таб")


class TabUpdate(TabBase):
    """Схема для обновления таба"""
    pass


class TabResponse(TabBase):
    """Схема ответа с данными таба"""
    id: int
    project_id: int
    
    class Config:
        from_attributes = True  # Для конвертации из SQLAlchemy модели

class Tab_deep_Response(TabResponse):
    """"""
    columns: List[Column_deep_Response] = []
    class Config:
        from_attributes = True  # Для конвертации из SQLAlchemy модели


class ReorderTabsRequest(BaseModel):
    """Схема запроса для изменения порядка табов"""
    tab_ids: List[int] = Field(..., description="Список ID табов в новом порядке")