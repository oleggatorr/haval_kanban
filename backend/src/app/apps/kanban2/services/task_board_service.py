from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.tasks.TaskBoard import TaskBoard
from ..schemas.task_board import TaskBoardCreate, TaskBoardUpdate


class TaskBoardService:
    """Сервис для работы с досками задач."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_board_by_id(self, board_id: int) -> Optional[TaskBoard]:
        """Получить доску по ID с загрузкой связей."""
        query = (
            select(TaskBoard)
            .options(
                selectinload(TaskBoard.columns),
                selectinload(TaskBoard.board_users),
                selectinload(TaskBoard.project)
            )
            .where(TaskBoard.id == board_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_board_by_project_id(self, project_id: int) -> Optional[TaskBoard]:
        """Получить доску по ID проекта (связь 1:1)."""
        query = (
            select(TaskBoard)
            .options(
                selectinload(TaskBoard.columns),
                selectinload(TaskBoard.board_users)
            )
            .where(TaskBoard.project_id == project_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_boards(
        self,
        page: int = 1,
        page_size: int = 10,
        is_active: Optional[bool] = None,
        project_id: Optional[int] = None
    ) -> tuple[list[TaskBoard], int]:
        """Получить список досок с пагинацией и фильтрами."""
        
        query = select(TaskBoard)
        count_query = select(func.count()).select_from(TaskBoard)
        
        # Фильтры
        if is_active is not None:
            query = query.where(TaskBoard.is_active == is_active)
            count_query = count_query.where(TaskBoard.is_active == is_active)
        
        if project_id is not None:
            query = query.where(TaskBoard.project_id == project_id)
            count_query = count_query.where(TaskBoard.project_id == project_id)
        
        # Общее количество
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Пагинация
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(TaskBoard.create_at.desc())
        
        result = await self.db.execute(query)
        boards = result.scalars().all()
        
        return list(boards), total
    
    async def create_board(self, board_data: TaskBoardCreate) -> TaskBoard:
        """Создать новую доску задач."""
        
        # Проверяем, не существует ли уже доска для этого проекта
        existing = await self.get_board_by_project_id(board_data.project_id)
        if existing:
            raise ValueError(f"Доска для проекта {board_data.project_id} уже существует")
        
        board = TaskBoard(
            project_id=board_data.project_id,
            name=board_data.name,
            description=board_data.description,
            is_active=True
        )
        
        self.db.add(board)
        await self.db.commit()
        await self.db.refresh(board)
        
        return board
    
    async def update_board(
        self,
        board_id: int,
        board_data: TaskBoardUpdate
    ) -> Optional[TaskBoard]:
        """Частично обновить доску задач."""
        
        board = await self.get_board_by_id(board_id)
        if not board:
            return None
        
        if board_data.name is not None:
            board.name = board_data.name
        
        if board_data.description is not None:
            board.description = board_data.description
        
        if board_data.is_active is not None:
            board.is_active = board_data.is_active
        
        await self.db.commit()
        await self.db.refresh(board)
        
        return board
    
    async def update_last_activity(self, board_id: int) -> bool:
        """Обновить timestamp последней активности доски."""
        
        board = await self.get_board_by_id(board_id)
        if not board:
            return False
        
        board.last_activity_at = datetime.now(timezone.utc)
        await self.db.commit()
        return True
    
    async def delete_board(self, board_id: int) -> bool:
        """Мягко удалить доску задач."""
        
        board = await self.get_board_by_id(board_id)
        if not board:
            return False
        
        board.is_active = False
        board.remove_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        return True
    
    async def hard_delete_board(self, board_id: int) -> bool:
        """Полностью удалить доску (каскадно удалит колонки и пользователей)."""
        
        board = await self.get_board_by_id(board_id)
        if not board:
            return False
        
        await self.db.delete(board)
        await self.db.commit()
        return True