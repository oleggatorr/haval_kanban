from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...models.tasks.SubTask import SubTask
from ...models.tasks.SubTaskUser import SubTaskUser
from ...schemas.tasks.subtask import SubTaskCreate, SubTaskUpdate
from ...models.other.TaskStatus import TaskStatus


class SubTaskService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    # ---------- helpers ----------

    async def _get_default_status_id(self) -> Optional[int]:
        """ID статуса по умолчанию (is_default=True, is_active=True)."""
        res = await self.db.execute(
            select(TaskStatus.id)
            .where(TaskStatus.is_default == True, TaskStatus.is_active == True)
            .limit(1)
        )
        return res.scalar_one_or_none()

    async def _get_status(self, status_id: int) -> Optional[TaskStatus]:
        """Получить активный статус по ID."""
        res = await self.db.execute(
            select(TaskStatus).where(
                TaskStatus.id == status_id,
                TaskStatus.is_active == True,
            )
        )
        return res.scalar_one_or_none()

    # ---------- read ----------

    async def get_subtask_by_id(self, subtask_id: int) -> Optional[SubTask]:
        """Получить подзадачу по ID."""
        query = (
            select(SubTask)
            .options(
                selectinload(SubTask.status),
                selectinload(SubTask.users),
                selectinload(SubTask.parent_task)
            )
            .where(SubTask.id == subtask_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_subtasks_by_parent(self, parent_task_id: int) -> List[SubTask]:
        """Получить все подзадачи родительской задачи."""
        query = (
            select(SubTask)
            .options(
                selectinload(SubTask.status),
                selectinload(SubTask.users)
            )
            .where(SubTask.parent_task_id == parent_task_id, SubTask.is_active == True)
            .order_by(SubTask.position.asc(), SubTask.id.asc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ---------- write ----------

    async def create_subtask(self, data: SubTaskCreate) -> SubTask:
        """Создать подзадачу. Если status_id не передан — ставим дефолтный."""
        status_id = data.status_id
        if status_id is None:
            status_id = await self._get_default_status_id()
            if status_id is None:
                raise ValueError("Статус по умолчанию не найден")

        # Автопозиционирование
        if data.position is None:
            max_pos = await self._get_max_position(data.parent_task_id)
            data.position = (max_pos or 0) + 1

        subtask = SubTask(
            parent_task_id=data.parent_task_id,
            status_id=status_id,
            name=data.name,
            description=data.description,
            position=data.position,
            date_time_start=data.date_time_start,
            date_time_end=data.date_time_end,
            planing_date_time_start=data.planing_date_time_start,
            planing_date_time_end=data.planing_date_time_end,
            is_active=True
        )

        self.db.add(subtask)
        await self.db.flush()

        # Добавляем пользователей
        if data.users:
            for u in data.users:
                self.db.add(SubTaskUser(
                    sub_task_id=subtask.id,
                    user_id=u.user_id,
                    role=u.role
                ))

        await self.db.commit()
        await self.db.refresh(subtask)
        await self.db.refresh(subtask, ['users', 'status'])
        return subtask

    async def change_status(self, subtask_id: int, status_id: int) -> Optional[SubTask]:
        """Сменить статус подзадачи."""
        subtask = await self.get_subtask_by_id(subtask_id)
        if not subtask:
            return None

        status = await self._get_status(status_id)
        if not status:
            raise ValueError(f"Статус {status_id} не найден или неактивен")

        subtask.status_id = status.id
        await self.db.commit()
        await self.db.refresh(subtask)
        await self.db.refresh(subtask, ['users', 'status'])
        return subtask

    async def update_subtask(self, subtask_id: int, data: SubTaskUpdate) -> Optional[SubTask]:
        """Обновить подзадачу."""
        subtask = await self.get_subtask_by_id(subtask_id)
        if not subtask:
            return None

        fields = [
            'name', 'description', 'position', 'status_id',
            'date_time_start', 'date_time_end',
            'planing_date_time_start', 'planing_date_time_end', 'is_active'
        ]

        for field in fields:
            val = getattr(data, field)
            if val is not None:
                setattr(subtask, field, val)

        await self.db.commit()
        await self.db.refresh(subtask)
        await self.db.refresh(subtask, ['users', 'status'])
        return subtask

    async def reorder_subtasks(self, parent_task_id: int, ids: List[int]) -> bool:
        """Изменить порядок подзадач."""
        for idx, sid in enumerate(ids):
            st = await self.get_subtask_by_id(sid)
            if not st or st.parent_task_id != parent_task_id:
                raise ValueError(f"SubTask {sid} invalid or belongs to another task")
            st.position = idx + 1
        await self.db.commit()
        return True

    async def delete_subtask(self, subtask_id: int, hard: bool = False) -> bool:
        """Удалить подзадачу."""
        subtask = await self.get_subtask_by_id(subtask_id)
        if not subtask:
            return False

        if hard:
            await self.db.delete(subtask)
        else:
            subtask.is_active = False
            subtask.remove_at = datetime.now(timezone.utc)

        await self.db.commit()
        return True

    async def _get_max_position(self, parent_task_id: int) -> Optional[int]:
        res = await self.db.execute(
            select(func.max(SubTask.position)).where(SubTask.parent_task_id == parent_task_id)
        )
        return res.scalar()