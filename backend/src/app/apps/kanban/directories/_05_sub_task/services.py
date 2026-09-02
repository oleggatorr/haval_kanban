# src\app\apps\kanban\directories\_05_sub_task\services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.sql import func

from .models import Sub_Task
from .._03_column.models import Column
from .._04_task.models import Task
from .._04_task.services import TaskService

from .schemas import SubTaskCreate, SubTaskUpdate, SubTaskResponse


class SubTaskService:
    """Сервис для работы с подзадачами"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_task_exists(self, task_id: int) -> bool:
        """Проверка существования родительской задачи"""
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none() is not None

    async def _touch_task(self, task_id: int) -> None:
        """
        Обновление временной метки задачи
        
        Args:
            task_id: ID задачи
        """
        task_service = TaskService(self.db)
        await task_service.touch_task(task_id)

    async def _get_sub_task(self, sub_task_id: int) -> Optional[Sub_Task]:
        """Вспомогательный метод: получение подзадачи по ID"""
        result = await self.db.execute(
            select(Sub_Task).where(Sub_Task.id == sub_task_id)
        )
        return result.scalar_one_or_none()

    async def _get_sub_task_response(self, sub_task_id: int) -> SubTaskResponse:
        """
        Вспомогательный метод: получает подзадачу и возвращает в формате ответа.
        """
        sub_task = await self._get_sub_task(sub_task_id)
        
        if not sub_task:
            raise HTTPException(
                status_code=404,
                detail=f"Подзадача с ID {sub_task_id} не найдена"
            )

        return SubTaskResponse(
            id=sub_task.id,
            tasks_id=sub_task.tasks_id,
            name=sub_task.name,
            order_id=sub_task.order_id
        )

    async def create_sub_task(self, sub_task_data: SubTaskCreate) -> SubTaskResponse:
        """Создание новой подзадачи"""
        if not await self._check_task_exists(sub_task_data.tasks_id):
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {sub_task_data.tasks_id} не существует"
            )
        
        # Определяем order_id, если не указан
        if sub_task_data.order_id is None:
            # Получаем максимальный order_id для данной задачи
            result = await self.db.execute(
                select(Sub_Task.order_id)
                .where(Sub_Task.tasks_id == sub_task_data.tasks_id)
                .order_by(Sub_Task.order_id.desc())
                .limit(1)
            )
            max_order = result.scalar_one_or_none()
            order_id = (max_order or 0) + 1
        else:
            order_id = sub_task_data.order_id
        
        db_sub_task = Sub_Task(
            tasks_id=sub_task_data.tasks_id,
            name=sub_task_data.name,
            order_id=order_id
        )
        
        self.db.add(db_sub_task)
        await self.db.commit()
        await self.db.refresh(db_sub_task)
        
        # Нормализуем порядки и обновляем задачу
        await self.normalize_sub_task_orders(sub_task_data.tasks_id)
        await self._touch_task(sub_task_data.tasks_id)
        
        return await self._get_sub_task_response(db_sub_task.id)

    async def get_sub_task_by_id(self, sub_task_id: int) -> Optional[SubTaskResponse]:
        """Получение подзадачи по ID"""
        try:
            return await self._get_sub_task_response(sub_task_id)
        except HTTPException:
            return None

    async def get_sub_tasks_by_task_id(self, task_id: int) -> List[SubTaskResponse]:
        """Получение всех подзадач задачи"""
        if not await self._check_task_exists(task_id):
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {task_id} не существует"
            )
        
        result = await self.db.execute(
            select(Sub_Task)
            .where(Sub_Task.tasks_id == task_id)
            .order_by(Sub_Task.order_id)
        )
        sub_tasks = result.scalars().all()
        
        return [
            SubTaskResponse(
                id=st.id,
                tasks_id=st.tasks_id,
                name=st.name,
                order_id=st.order_id
            )
            for st in sub_tasks
        ]

    async def get_all_sub_tasks(self) -> List[SubTaskResponse]:
        """Получение всех подзадач"""
        result = await self.db.execute(select(Sub_Task).order_by(Sub_Task.tasks_id, Sub_Task.order_id))
        sub_tasks = result.scalars().all()
        
        return [
            SubTaskResponse(
                id=st.id,
                tasks_id=st.tasks_id,
                name=st.name,
                order_id=st.order_id
            )
            for st in sub_tasks
        ]

    async def update_sub_task(
        self, 
        sub_task_id: int, 
        sub_task_data: SubTaskUpdate
    ) -> Optional[SubTaskResponse]:
        """Обновление подзадачи"""
        sub_task = await self._get_sub_task(sub_task_id)
        
        if not sub_task:
            return None
        
        task_id = sub_task.tasks_id
        
        # Обновляем поля подзадачи
        if sub_task_data.name is not None:
            sub_task.name = sub_task_data.name
            
        if sub_task_data.order_id is not None:
            # Просто обновляем order_id без проверки на уникальность
            # Сортировка будет происходить по order_id, а при равных значениях - по id
            sub_task.order_id = sub_task_data.order_id
        
        await self.db.commit()
        await self.db.refresh(sub_task)
        
        # Обновляем задачу
        await self._touch_task(task_id)
        
        return await self._get_sub_task_response(sub_task_id)

    async def delete_sub_task(self, sub_task_id: int) -> bool:
        """Удаление подзадачи"""
        sub_task = await self._get_sub_task(sub_task_id)
        
        if not sub_task:
            return False
        
        task_id = sub_task.tasks_id
        
        await self.db.delete(sub_task)
        await self.db.commit()
        
        # Нормализуем порядки и обновляем задачу
        await self.normalize_sub_task_orders(task_id)
        await self._touch_task(task_id)
        
        return True

    async def delete_sub_tasks_by_task_id(self, task_id: int) -> int:
        """Удаление всех подзадач задачи"""
        if not await self._check_task_exists(task_id):
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {task_id} не существует"
            )
        
        result = await self.db.execute(
            delete(Sub_Task).where(Sub_Task.tasks_id == task_id)
        )
        await self.db.commit()
        
        # Обновляем задачу
        await self._touch_task(task_id)
        
        return result.rowcount

    async def normalize_sub_task_orders(self, task_id: int) -> List[SubTaskResponse]:
        """Нормализация порядковых номеров подзадач для конкретной задачи"""
        if not await self._check_task_exists(task_id):
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {task_id} не существует"
            )
        
        result = await self.db.execute(
            select(Sub_Task)
            .where(Sub_Task.tasks_id == task_id)
            .order_by(Sub_Task.order_id, Sub_Task.id)
        )
        sub_tasks = result.scalars().all()
        
        for index, sub_task in enumerate(sub_tasks, start=1):
            sub_task.order_id = index
        
        await self.db.commit()
        
        # Обновляем задачу после нормализации
        await self._touch_task(task_id)
        
        return [
            SubTaskResponse(
                id=st.id,
                tasks_id=st.tasks_id,
                name=st.name,
                order_id=st.order_id
            )
            for st in sub_tasks
        ]

    async def reorder_sub_tasks(self, task_id: int, new_order: List[int]) -> List[SubTaskResponse]:
        """Изменение порядка подзадач для конкретной задачи"""
        if not await self._check_task_exists(task_id):
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {task_id} не существует"
            )
        
        if not new_order:
            raise HTTPException(
                status_code=400,
                detail="Список ID подзадач не может быть пустым"
            )
        
        result = await self.db.execute(
            select(Sub_Task).where(Sub_Task.tasks_id == task_id)
        )
        existing_sub_tasks = result.scalars().all()
        existing_sub_task_ids = {st.id for st in existing_sub_tasks}
        
        new_order_set = set(new_order)
        if not new_order_set.issubset(existing_sub_task_ids):
            invalid_ids = new_order_set - existing_sub_task_ids
            raise HTTPException(
                status_code=400,
                detail=f"Подзадачи с ID {invalid_ids} не принадлежат задаче {task_id}"
            )
        
        if len(new_order) != len(existing_sub_tasks):
            raise HTTPException(
                status_code=400,
                detail=f"Количество ID в списке ({len(new_order)}) не совпадает "
                       f"с количеством подзадач задачи ({len(existing_sub_tasks)})"
            )
        
        for index, sub_task_id in enumerate(new_order, start=1):
            sub_task = next((st for st in existing_sub_tasks if st.id == sub_task_id), None)
            if sub_task:
                sub_task.order_id = index
        
        await self.db.commit()
        
        # Обновляем задачу
        await self._touch_task(task_id)
        
        result = await self.db.execute(
            select(Sub_Task)
            .where(Sub_Task.tasks_id == task_id)
            .order_by(Sub_Task.order_id)
        )
        reordered_sub_tasks = result.scalars().all()
        
        return [
            SubTaskResponse(
                id=st.id,
                tasks_id=st.tasks_id,
                name=st.name,
                order_id=st.order_id
            )
            for st in reordered_sub_tasks
        ]

    async def get_sub_task_count_by_task_id(self, task_id: int) -> int:
        """Получение количества подзадач для задачи"""
        result = await self.db.execute(
            select(Sub_Task)
            .where(Sub_Task.tasks_id == task_id)
        )
        return len(result.scalars().all())

    # ============ МЕТОДЫ ДЛЯ "КАСАНИЯ" ============

    async def touch_sub_task(self, sub_task_id: int) -> Optional[SubTaskResponse]:
        """
        Обновление только поля updated_at подзадачи и связанной задачи
        
        Используется для обновления временной метки без изменения данных.
        
        Args:
            sub_task_id: ID подзадачи
            
        Returns:
            Обновленная подзадача или None если не найдена
        """
        sub_task = await self._get_sub_task(sub_task_id)
        
        if not sub_task:
            return None
        
        task_id = sub_task.tasks_id
        
        # Принудительно обновляем updated_at подзадачи
        sub_task.updated_at = func.now()
        
        await self.db.commit()
        await self.db.refresh(sub_task)
        
        # Обновляем задачу
        await self._touch_task(task_id)
        
        return await self._get_sub_task_response(sub_task_id)

    async def touch_sub_tasks_by_task(self, task_id: int) -> List[SubTaskResponse]:
        """
        Обновление поля updated_at для всех подзадач задачи
        
        Args:
            task_id: ID задачи
            
        Returns:
            Список обновленных подзадач
            
        Raises:
            HTTPException: Если задача не существует
        """
        if not await self._check_task_exists(task_id):
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {task_id} не существует"
            )
        
        # Получаем все подзадачи задачи
        result = await self.db.execute(
            select(Sub_Task).where(Sub_Task.tasks_id == task_id)
        )
        sub_tasks = result.scalars().all()
        
        if not sub_tasks:
            return []
        
        # Обновляем updated_at для всех подзадач
        now = func.now()
        for sub_task in sub_tasks:
            sub_task.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for sub_task in sub_tasks:
            await self.db.refresh(sub_task)
        
        # Обновляем задачу
        await self._touch_task(task_id)
        
        return [
            SubTaskResponse(
                id=st.id,
                tasks_id=st.tasks_id,
                name=st.name,
                order_id=st.order_id
            )
            for st in sub_tasks
        ]

    async def bulk_touch_sub_tasks(self, sub_task_ids: List[int]) -> List[SubTaskResponse]:
        """
        Массовое обновление поля updated_at для нескольких подзадач
        
        Args:
            sub_task_ids: Список ID подзадач
            
        Returns:
            Список обновленных подзадач
        """
        if not sub_task_ids:
            return []
        
        # Получаем все подзадачи по списку ID
        result = await self.db.execute(
            select(Sub_Task).where(Sub_Task.id.in_(sub_task_ids))
        )
        sub_tasks = result.scalars().all()
        
        if not sub_tasks:
            return []
        
        # Сохраняем уникальные task_id для обновления
        task_ids = {sub_task.tasks_id for sub_task in sub_tasks}
        
        # Обновляем updated_at для всех найденных подзадач
        now = func.now()
        for sub_task in sub_tasks:
            sub_task.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for sub_task in sub_tasks:
            await self.db.refresh(sub_task)
        
        # Обновляем все затронутые задачи
        for task_id in task_ids:
            await self._touch_task(task_id)
        
        return [
            SubTaskResponse(
                id=st.id,
                tasks_id=st.tasks_id,
                name=st.name,
                order_id=st.order_id
            )
            for st in sub_tasks
        ]