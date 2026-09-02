from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.app.zup.users.schemas import EmployeeResponse


class UserBase(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    employee_id: str = Field(..., min_length=1, max_length=50, description="Табельный номер сотрудника")


class UserUpdate(BaseModel):
    login: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)


class UserResponse(UserBase):
    """Базовый ответ по пользователю (только локальные данные)."""
    model_config = ConfigDict(from_attributes=True)

    employee_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserFullResponse(UserResponse):
    """Расширенный ответ с данными из кадровой системы ZUP."""
    zup_info: Optional[EmployeeResponse] = None
    warning: Optional[str] = None