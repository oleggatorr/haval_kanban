from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.tasks.TaskColumn import TaskColumn
from ..schemas.task_column import TaskColumnCreate, TaskColumnUpdate


class TaskColumnService:
    """Сервис для работы с колонками задач."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_column_by_id(self, column_id: int) -> Optional[TaskColumn]:
        """Получить колонку по ID."""
        query = (
            select(TaskColumn)
            .options(
                selectinload(TaskColumn.tasks),
                selectinload(TaskColumn.board)
            )
            .where(TaskColumn.id == column_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_columns_by_board(
        self,
        board_id: int,
        is_active: Optional[bool] = None
    ) -> List[TaskColumn]:
        """Получить все колонки доски, отсортированные по позиции."""
        
        query = (
            select(TaskColumn)
            .options(selectinload(TaskColumn.tasks))
            .where(TaskColumn.board_id == board_id)
        )
        
        if is_active is not None:
            query = query.where(TaskColumn.is_active == is_active)
        
        # Сортируем по позиции, затем по ID
        query = query.order_by(TaskColumn.position.asc(), TaskColumn.id.asc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_columns_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        board_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> tuple[list[TaskColumn], int]:
        """Получить список колонок с пагинацией."""
        
        query = select(TaskColumn)
        count_query = select(func.count()).select_from(TaskColumn)
        
        # Фильтры
        if board_id is not None:
            query = query.where(TaskColumn.board_id == board_id)
            count_query = count_query.where(TaskColumn.board_id == board_id)
        
        if is_active is not None:
            query = query.where(TaskColumn.is_active == is_active)
            count_query = count_query.where(TaskColumn.is_active == is_active)
        
        # Общее количество
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Пагинация
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(
            TaskColumn.board_id.asc(),
            TaskColumn.position.asc(),
            TaskColumn.id.asc()
        )
        
        result = await self.db.execute(query)
        columns = result.scalars().all()
        
        return list(columns), total
    
    async def create_column(self, column_data: TaskColumnCreate) -> TaskColumn:
        """Создать новую колонку задач."""
        
        # Определяем позицию: если не указана, ставим в конец
        if column_data.position is None:
            max_position = await self._get_max_position(column_data.board_id)
            column_data.position = (max_position or 0) + 1
        
        column = TaskColumn(
            board_id=column_data.board_id,
            name=column_data.name,
            description=column_data.description,
            flags=column_data.flags,
            position=column_data.position,
            is_active=True
        )
        
        self.db.add(column)
        await self.db.commit()
        await self.db.refresh(column)
        
        return column
    
    async def update_column(
        self,
        column_id: int,
        column_data: TaskColumnUpdate
    ) -> Optional[TaskColumn]:
        """Частично обновить колонку."""
        
        column = await self.get_column_by_id(column_id)
        if not column:
            return None
        
        if column_data.name is not None:
            column.name = column_data.name
        
        if column_data.description is not None:
            column.description = column_data.description
        
        if column_data.flags is not None:
            column.flags = column_data.flags
        
        if column_data.position is not None:
            column.position = column_data.position
        
        if column_data.is_active is not None:
            column.is_active = column_data.is_active
        
        await self.db.commit()
        await self.db.refresh(column)
        
        return column
    
    async def reorder_columns(
        self,
        board_id: int,
        column_ids: List[int]
    ) -> bool:
        """Изменить порядок колонок на доске."""
        
        # Проверяем, что все колонки принадлежат этой доске
        for idx, column_id in enumerate(column_ids):
            column = await self.get_column_by_id(column_id)
            
            if not column:
                raise ValueError(f"Колонка с ID {column_id} не найдена")
            
            if column.board_id != board_id:
                raise ValueError(f"Колонка {column_id} не принадлежит доске {board_id}")
            
            # Обновляем позицию
            column.position = idx + 1
        
        await self.db.commit()
        return True
    
    async def delete_column(self, column_id: int) -> bool:
        """Мягко удалить колонку."""
        
        column = await self.get_column_by_id(column_id)
        if not column:
            return False
        
        column.is_active = False
        column.remove_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        return True
    
    async def hard_delete_column(self, column_id: int) -> bool:
        """Полностью удалить колонку (каскадно удалит задачи)."""
        
        column = await self.get_column_by_id(column_id)
        if not column:
            return False
        
        await self.db.delete(column)
        await self.db.commit()
        return True
    
    async def _get_max_position(self, board_id: int) -> Optional[int]:
        """Получить максимальную позицию колонки на доске."""
        
        query = (
            select(func.max(TaskColumn.position))
            .where(TaskColumn.board_id == board_id)
        )
        
        result = await self.db.execute(query)
        return result.scalar()