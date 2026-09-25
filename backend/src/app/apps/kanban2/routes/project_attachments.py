from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json

from src.core.database.connection import get_db
from src.app.apps.kanban2.services.project_attachment_service import AttachmentService
from src.app.apps.kanban2.schemas.project_attachment import ProjectAttachmentResponse, ProjectAttachmentUpdate, AttachmentUploadForm

router = APIRouter(prefix="/projects/{project_id}/attachments", tags=["Attachments"])


@router.post("/", response_model=ProjectAttachmentResponse)
async def upload_attachment(
    project_id: int,
    file: UploadFile = File(...),
    form_data: AttachmentUploadForm = Depends(), # <-- Внедряем форму через Depends
    db: AsyncSession = Depends(get_db)
):
    """Загрузка нового вложения к проекту."""
    
    # Безопасный парсинг JSON из формы
    meta_dict = None
    if form_data.metadata and form_data.metadata.strip():
        try:
            meta_dict = json.loads(form_data.metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Неверный формат JSON в поле metadata")
    
    try:
        attachment = await AttachmentService.create_attachment(db, project_id, file, meta_dict)
        return attachment
    except Exception as e:
        print(f"Error uploading file: {e}") 
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки: {str(e)}")


@router.get("/", response_model=List[ProjectAttachmentResponse])
async def list_attachments(project_id: int, db: AsyncSession = Depends(get_db)):
    """Список всех вложений проекта."""
    return await AttachmentService.get_attachments_by_project(db, project_id)


@router.patch("/{attachment_id}", response_model=ProjectAttachmentResponse)
async def update_attachment(
    project_id: int,
    attachment_id: int,
    update_data: ProjectAttachmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Редактирование информации о вложении."""
    updated = await AttachmentService.update_attachment_info(db, attachment_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Вложение не найдено")
    return updated


@router.delete("/{attachment_id}")
async def delete_attachment(project_id: int, attachment_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление вложения."""
    success = await AttachmentService.delete_attachment(db, attachment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Вложение не найдено")
    return {"message": "Вложение успешно удалено"}