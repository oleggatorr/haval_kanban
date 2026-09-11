from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProjectDataBase(BaseModel):
    """Базовая схема для дополнительных данных проекта."""
    
    big_description: Optional[str] = Field(None, description="Подробное описание проекта")


class ProjectDataCreate(ProjectDataBase):
    """Схема для создания дополнительных данных проекта."""
    pass


class ProjectDataUpdate(ProjectDataBase):
    """Схема для обновления дополнительных данных проекта."""
    
    big_description: Optional[str] = Field(None, description="Подробное описание проекта")


class ProjectDataResponse(ProjectDataBase):
    """Схема ответа для дополнительных данных проекта."""
    
    id: int
    project_id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    remove_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    """Базовая схема проекта."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Название проекта")


class ProjectCreate(ProjectBase):
    """Схема для создания проекта."""
    
    data: Optional[ProjectDataCreate] = Field(None, description="Дополнительные данные проекта")


class ProjectUpdate(BaseModel):
    """Схема для обновления проекта."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Название проекта")
    is_active: Optional[bool] = Field(None, description="Статус активности проекта")
    data: Optional[ProjectDataUpdate] = Field(None, description="Дополнительные данные проекта")


class ProjectResponse(ProjectBase):
    """Схема ответа для проекта."""
    
    id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    is_active: bool
    remove_at: Optional[datetime] = None
    data: Optional[ProjectDataResponse] = None
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Схема ответа для списка проектов."""
    
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int