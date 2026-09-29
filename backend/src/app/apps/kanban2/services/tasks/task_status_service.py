from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.other.TaskStatus import TaskStatus
from ...schemas.tasks.task_status import TaskStatusCreate, TaskStatusUpdate


class TaskStatusService:
    """Сервис для работы со статусами задач."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = False
    ) -> tuple[list[TaskStatus], int]:
        """Получить список всех статусов задач с пагинацией."""
        
        query = select(TaskStatus)
        count_query = select(func.count(TaskStatus.id))
        
        if active_only:
            query = query.where(TaskStatus.is_active == True)
            count_query = count_query.where(TaskStatus.is_active == True)
        
        query = query.offset(skip).limit(limit).order_by(TaskStatus.id)
        
        result = await self.db.execute(query)
        statuses = result.scalars().all()
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        return list(statuses), total
    
    async def get_by_id(self, status_id: int) -> Optional[TaskStatus]:
        """Получить статус задачи по ID."""
        
        query = select(TaskStatus).where(TaskStatus.id == status_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, status_data: TaskStatusCreate) -> TaskStatus:
        """Создать новый статус задачи."""
        
        # Проверяем, не существует ли уже статус с таким именем
        existing_query = select(TaskStatus).where(TaskStatus.name == status_data.name)
        existing_result = await self.db.execute(existing_query)
        if existing_result.scalar_one_or_none():
            raise ValueError(f"Статус с названием '{status_data.name}' уже существует")
        
        # Если это статус по умолчанию, снимаем флаг у других
        if status_data.is_default:
            await self._unset_default_status()
        
        new_status = TaskStatus(
            name=status_data.name,
            description=status_data.description,
            is_default=status_data.is_default,
            is_final=status_data.is_final,
            is_active=status_data.is_active,
            create_at=datetime.now(timezone.utc)
        )
        
        self.db.add(new_status)
        await self.db.commit()
        await self.db.refresh(new_status)
        
        return new_status
    
    async def update(
        self, 
        status_id: int, 
        status_data: TaskStatusUpdate
    ) -> Optional[TaskStatus]:
        """Обновить статус задачи."""
        
        status = await self.get_by_id(status_id)
        if not status:
            return None
        
        update_data = status_data.model_dump(exclude_unset=True)
        
        # Если устанавливаем is_default, снимаем флаг у других
        if update_data.get('is_default', False):
            await self._unset_default_status(exclude_id=status_id)
        
        for field, value in update_data.items():
            setattr(status, field, value)
        
        status.update_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        await self.db.refresh(status)
        
        return status
    
    async def delete(self, status_id: int) -> bool:
        """Мягко удалить статус задачи (установить remove_at)."""
        
        status = await self.get_by_id(status_id)
        if not status:
            return False
        
        status.is_active = False
        status.remove_at = datetime.now(timezone.utc)
        status.update_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        return True
    
    async def hard_delete(self, status_id: int) -> bool:
        """Полностью удалить статус задачи."""
        
        status = await self.get_by_id(status_id)
        if not status:
            return False
        
        await self.db.delete(status)
        await self.db.commit()
        return True
    
    async def _unset_default_status(self, exclude_id: Optional[int] = None):
        """Снять флаг is_default у всех статусов, кроме указанного."""
        
        query = select(TaskStatus).where(TaskStatus.is_default == True)
        if exclude_id:
            query = query.where(TaskStatus.id != exclude_id)
        
        result = await self.db.execute(query)
        default_statuses = result.scalars().all()
        
        for status in default_statuses:
            status.is_default = False
            status.update_at = datetime.now(timezone.utc)
        
        await self.db.flush()
        
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = False
    ) -> tuple[list[TaskStatus], int]:
        """Получить список всех статусов задач с пагинацией."""
        
        query = select(TaskStatus)
        count_query = select(func.count(TaskStatus.id))
        
        if active_only:
            query = query.where(TaskStatus.is_active == True)
            count_query = count_query.where(TaskStatus.is_active == True)
        
        query = query.offset(skip).limit(limit).order_by(TaskStatus.id)
        
        result = await self.db.execute(query)
        statuses = result.scalars().all()
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        return list(statuses), total

    async def get_all_statuses(self, active_only: bool = False) -> list[TaskStatus]:
        """Получить все статусы задач без пагинации."""
        
        query = select(TaskStatus).order_by(TaskStatus.id)
        
        if active_only:
            query = query.where(TaskStatus.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())