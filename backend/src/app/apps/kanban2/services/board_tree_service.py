from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.projects.Project import Project
from ..models.tasks.TaskBoard import TaskBoard
from ..models.tasks.TaskColumn import TaskColumn
from ..models.tasks.Task import Task
from ..schemas.tree import ProjectTreeResponse, BoardTree, ColumnTree, TaskTree


class BoardTreeService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_full_board_tree(self, project_id: int) -> Optional[ProjectTreeResponse]:
        """Получить полное дерево проекта."""
        
        query = (
            select(Project)
            .options(
                selectinload(Project.task_board)
                .options(
                    selectinload(TaskBoard.columns)
                    .options(
                        selectinload(TaskColumn.tasks)
                        .options(
                            selectinload(Task.data),
                            selectinload(Task.users)
                        )
                    )
                )
            )
            .where(Project.id == project_id)
        )
        
        result = await self.db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            return None

        # Проверяем, что task_board действительно существует и является объектом TaskBoard
        board = project.task_board
        if not board:
            return None
            
        # Дополнительная проверка типа для отладки
        if not isinstance(board, TaskBoard):
            print(f"DEBUG: Unexpected type for board: {type(board)}, value: {board}")
            return None

        # Получаем колонки. Если board.columns - это InstrumentedList, он ведет себя как список.
        columns = board.columns
        
        # Сортируем колонки по позиции
        # Используем getattr для безопасности, если position отсутствует
        sorted_columns = sorted(columns, key=lambda c: getattr(c, 'position', 0) or 0)
        
        column_trees = []
        for col in sorted_columns:
            tasks = col.tasks if col.tasks else []
            
            # Сортируем задачи
            sorted_tasks = sorted(tasks, key=lambda t: getattr(t, 'position', 0) or 0)
            
            # Фильтруем активные задачи и преобразуем
            task_trees = [
                TaskTree.model_validate(t) for t in sorted_tasks if getattr(t, 'is_active', False)
            ]
            
            column_trees.append(ColumnTree(
                id=col.id,
                name=col.name,
                description=col.description,
                position=col.position,
                flags=col.flags,
                tasks=task_trees
            ))

        board_tree = BoardTree(
            id=board.id,
            project_id=board.project_id,
            name=board.name,
            description=board.description,
            last_activity_at=board.last_activity_at,
            columns=column_trees
        )

        return ProjectTreeResponse(
            id=project.id,
            name=project.name,
            create_at=project.create_at,
            is_active=project.is_active,
            board=board_tree
        )