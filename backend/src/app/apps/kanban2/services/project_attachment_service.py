import os
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.app.apps.kanban2.models.projects.ProjectAttachment import ProjectAttachment
from src.app.apps.kanban2.schemas.project_attachment import ProjectAttachmentCreate, ProjectAttachmentUpdate
from src.core.storage.local_storage import LocalFileStorage
from loguru import logger

# Инициализируем хранилище (лучше вынести в конфиг или DI)
STORAGE_PATH = "./uploads/projects" 
file_storage = LocalFileStorage(STORAGE_PATH)


class AttachmentService:
    
    @staticmethod
    async def create_attachment(
        db: AsyncSession, 
        project_id: int, 
        file: UploadFile, 
        metadata: Optional[dict] = None
    ) -> ProjectAttachment:
        """Загружает файл и создает запись в БД."""
        
        # 1. Читаем контент
        content = await file.read()
        file_size = len(content)
        mime_type = file.content_type or "application/octet-stream"
        
        # 2. Сохраняем в файловую систему
        # LocalFileStorage.save вернет полный путь, но нам лучше хранить относительный или просто имя
        # Для простоты сохраним как есть, но в продакшене лучше хранить относительный путь
        stored_path = file_storage.save(content, file.filename)
        stored_name = os.path.basename(stored_path) # Получаем только имя файла из пути
        
        # 3. Создаем запись в БД
        new_attachment = ProjectAttachment(
            project_id=project_id,
            original_name=file.filename,
            stored_name=stored_name,
            file_size=file_size,
            mime_type=mime_type,
            file_metadata=metadata or {}
        )
        
        db.add(new_attachment)
        await db.commit()
        await db.refresh(new_attachment)
        
        return new_attachment

    @staticmethod
    async def get_attachments_by_project(db: AsyncSession, project_id: int) -> List[ProjectAttachment]:
        """Получает список всех вложений проекта."""
        result = await db.execute(
            select(ProjectAttachment).where(ProjectAttachment.project_id == project_id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_attachment_info(
        db: AsyncSession, 
        attachment_id: int, 
        update_data: ProjectAttachmentUpdate
    ) -> Optional[ProjectAttachment]:
        """Обновляет метаданные вложения (имя, описание и т.д.)."""
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
            
        stmt = update(ProjectAttachment).where(ProjectAttachment.id == attachment_id).values(**update_dict)
        await db.execute(stmt)
        await db.commit()
        
        # Возвращаем обновленный объект
        result = await db.execute(select(ProjectAttachment).where(ProjectAttachment.id == attachment_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_attachment(db: AsyncSession, attachment_id: int) -> bool:
        """Удаляет вложение из БД и с диска."""
        # 1. Находим запись, чтобы узнать путь к файлу
        result = await db.execute(select(ProjectAttachment).where(ProjectAttachment.id == attachment_id))
        attachment = result.scalar_one_or_none()
        
        if not attachment:
            return False
            
        # 2. Удаляем файл с диска
        # Важно: здесь нужно восстановить полный путь, если stored_name хранит только имя
        full_path = os.path.join(STORAGE_PATH, attachment.stored_name)
        file_storage.delete(full_path)
        
        # 3. Удаляем из БД
        await db.execute(delete(ProjectAttachment).where(ProjectAttachment.id == attachment_id))
        await db.commit()
        
        return True