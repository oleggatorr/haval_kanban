from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class EmployeeResponse(BaseModel):
    guid: str
    guid_person: Optional[str] = None
    employee_id: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name_en: Optional[str] = None
    first_name_en: Optional[str] = None
    middle_name_en: Optional[str] = None
    birth_date: Optional[date] = None
    employment_date: Optional[date] = None
    dismissal_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    position_guid: Optional[str] = None
    department_guid: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True