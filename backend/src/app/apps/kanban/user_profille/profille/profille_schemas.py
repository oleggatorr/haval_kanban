from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime

# Импорты схем из соседних модулей
from .....user_auth.users.schemas import UserResponse
from .....zup.users.schemas import EmployeeResponse


class UserProfileBase(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=150, description="Имя для отображения")
    permissions: dict[str, Any] = Field(default_factory=dict, description="Роли и права доступа")
    preferences: dict[str, Any] = Field(default_factory=dict, description="UI-настройки")
    is_active: bool = Field(default=True, description="Активен ли сотрудник")


class UserProfileCreate(UserProfileBase):
    employee_id: str = Field(..., min_length=1, max_length=20, description="ID сотрудника из auth_users")


class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=150)
    permissions: Optional[dict[str, Any]] = None
    preferences: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


class UserProfileResponse(UserProfileBase):
    """Базовый ответ профиля."""
    model_config = ConfigDict(from_attributes=True)

    employee_id: str
    created_at: datetime
    updated_at: datetime


class UserFullInfoResponse(BaseModel):
    """Полная информация: профиль + auth + ZUP."""
    model_config = ConfigDict(from_attributes=True)

    profile: UserProfileResponse
    auth: UserResponse
    zup_info: Optional[EmployeeResponse] = None
    warning: Optional[str] = None