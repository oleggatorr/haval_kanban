# src/app/kanban/_05_sub_task/schemas.py

from pydantic import BaseModel
from typing import Optional


class SubTaskBase(BaseModel):
    tasks_id: int
    name: Optional[str] = None
    order_id: Optional[int] = None


class SubTaskCreate(SubTaskBase):
    pass


class SubTaskUpdate(BaseModel):
    name: Optional[str] = None
    order_id: Optional[int] = None


class SubTaskResponse(BaseModel):
    id: int
    tasks_id: int
    name: Optional[str] = None
    order_id: Optional[int] = None
    
    class Config:
        from_attributes = True