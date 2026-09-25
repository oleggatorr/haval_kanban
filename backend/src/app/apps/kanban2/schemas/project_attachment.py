from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectAttachmentBase(BaseModel):
    original_name: str = Field(..., description="Имя файла при загрузке")
    file_metadata: Optional[dict] = Field(default_factory=dict, description="Дополнительные метаданные")


class ProjectAttachmentCreate(ProjectAttachmentBase):
    pass


class ProjectAttachmentUpdate(BaseModel):
    original_name: Optional[str] = None
    file_metadata: Optional[dict] = None


class ProjectAttachmentResponse(ProjectAttachmentBase):
    id: int
    project_id: int
    stored_name: str
    file_size: int
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class AttachmentUploadForm(BaseModel):
    metadata: Optional[str] = Field(None, description="JSON строка с метаданными")