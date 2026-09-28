from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import json
import os
from pathlib import Path
from loguru import logger
from fastapi.responses import FileResponse

from src.core.database.connection import get_db
from src.app.apps.kanban2.services.project_attachment_service import AttachmentService
from src.app.apps.kanban2.schemas.project_attachment import ProjectAttachmentResponse, ProjectAttachmentUpdate, AttachmentUploadForm
# Импортируем путь, который был определен в сервисе или вынесите его в конфиг
from src.app.apps.kanban2.services.project_attachment_service import STORAGE_PATH 

router = APIRouter(prefix="/projects/{project_id}/attachments", tags=["Attachments"])

@router.post("/", response_model=ProjectAttachmentResponse)
async def upload_attachment(
    project_id: int,
    file: UploadFile = File(...),
    form_data: AttachmentUploadForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Загрузка нового вложения к проекту."""
    
    meta_dict = None
    if form_data.metadata and form_data.metadata.strip():
        try:
            meta_dict = json.loads(form_data.metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Неверный формат JSON в поле metadata")
    
    try:
        # Передаем project_id в сервис для проверки существования проекта (если нужно)
        attachment = await AttachmentService.create_attachment(db, project_id, file, meta_dict)
        return attachment
    except Exception as e:
        logger.error(f"Error uploading file for project {project_id}: {e}") 
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
    # Желательно добавить проверку, что вложение действительно принадлежит этому проекту
    updated = await AttachmentService.update_attachment_info(db, attachment_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Вложение не найдено")
    
    # Дополнительная проверка безопасности: принадлежит ли вложение проекту?
    if updated.project_id != project_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен: вложение принадлежит другому проекту")
        
    return updated

@router.delete("/{attachment_id}")
async def delete_attachment(project_id: int, attachment_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление вложения."""
    # Аналогично, лучше проверять принадлежность перед удалением
    success = await AttachmentService.delete_attachment(db, attachment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Вложение не найдено")
    return {"message": "Вложение успешно удалено"}

@router.get("/{attachment_id}/download")
async def download_attachment(
    project_id: int, # Добавляем project_id для контекста и безопасности
    attachment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Скачивание файла вложения."""
    attachment = await AttachmentService.get_attachment_by_id(db, attachment_id)
    
    if not attachment:
        raise HTTPException(status_code=404, detail="Вложение не найдено")

    # Проверка безопасности: файл должен принадлежать запрашиваемому проекту
    if attachment.project_id != project_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # Используем Path для безопасного формирования пути
    base_path = Path(STORAGE_PATH)
    file_path = base_path / attachment.stored_name
    
    # Защита от Path Traversal: убеждаемся, что путь находится внутри base_path
    try:
        file_path.resolve().relative_to(base_path.resolve())
    except ValueError:
        raise HTTPException(status_code=400, detail="Небезопасный путь к файлу")

    if not file_path.exists():
        logger.error(f"Файл отсутствует на диске: {file_path}")
        raise HTTPException(status_code=500, detail="Файл поврежден или удален")
        
    return FileResponse(
        path=str(file_path),
        filename=attachment.original_name,
        media_type=attachment.mime_type
    )