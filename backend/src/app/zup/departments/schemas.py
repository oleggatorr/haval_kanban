from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

class DepartmentBase(BaseModel):
    guid: str
    name: str
    name_en: Optional[str] = None
    short_name: Optional[str] = None
    creation_date: Optional[date] = None
    closure_date: Optional[date] = None
    parent_guid: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class DepartmentRead(DepartmentBase):
    """Схема для чтения одного отдела"""
    model_config = ConfigDict(from_attributes=True)

class DepartmentTree(DepartmentBase):
    """Схема для отображения иерархии (вложенность)"""
    children: List["DepartmentTree"] = []
    model_config = ConfigDict(from_attributes=True)