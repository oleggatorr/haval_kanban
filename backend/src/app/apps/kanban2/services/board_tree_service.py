from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional

from ..models.projects.Project import Project
from ..models.tasks.TaskBoard import TaskBoard
from ..models.tasks.TaskColumn import TaskColumn
from ..models.tasks.Task import Task
from ..models.tasks.SubTask import SubTask
from ..schemas.tree2 import KanbanBoardResponse, BoardFlat, ColumnFlat, TaskFlat, SubtaskTree, UserSimple


class KanbanService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_kanban_data(self, project_id: int) -> Optional[KanbanBoardResponse]:
        query = (
            select(Project)
            .options(
                selectinload(Project.task_board).options(
                    selectinload(TaskBoard.columns).options(
                        selectinload(TaskColumn.tasks).options(
                            selectinload(Task.users),
                            selectinload(Task.data),
                            selectinload(Task.sub_tasks).options(
                                selectinload(SubTask.users)
                            ),
                        )
                    )
                )
            )
            .where(Project.id == project_id)
        )

        result = await self.db.execute(query)
        project = result.scalar_one_or_none()

        if not project or not project.task_board:
            return None

        board = project.task_board
        board_flat = BoardFlat.model_validate(board)

        flat_columns = []
        flat_tasks = []
        flat_subtasks = []

        sorted_columns = sorted(board.columns, key=lambda c: c.position or 0)

        for col in sorted_columns:
            flat_columns.append(ColumnFlat(
                id=col.id,
                board_id=board.id,
                name=col.name,
                description=col.description,
                position=col.position,
                flags=col.flags or []
            ))

            active_tasks = [t for t in col.tasks if t.is_active]
            sorted_tasks = sorted(active_tasks, key=lambda t: t.position or 0)

            for task in sorted_tasks:
                task_users = (
                    [UserSimple(id=u.id, name=u.name) for u in task.users]
                    if task.users else []
                )

                # Берём только активные подзадачи и сортируем по position
                task_subtasks = sorted(
                    [st for st in (task.sub_tasks or []) if st.is_active],
                    key=lambda st: st.position or 0,
                )

                completed_count = sum(
                    1 for st in task_subtasks if st.status_id == 3  # 3 = Done
                )

                flat_tasks.append(TaskFlat(
                    id=task.id,
                    column_id=col.id,
                    name=task.name,
                    description=task.description,
                    position=task.position,
                    status_id=task.status_id,
                    date_time_start=task.date_time_start,
                    date_time_end=task.date_time_end,
                    planing_date_time_start=task.planing_date_time_start,
                    planing_date_time_end=task.planing_date_time_end,
                    data=task.data,
                    users=task_users,
                    subtasks_count=len(task_subtasks),
                    completed_subtasks_count=completed_count,
                ))

                for st in task_subtasks:
                    # st.users — это SubTaskUser, а не User.
                    # Нужно пройти через .user (UserRole), чтобы получить id/name.
                    st_users = []
                    for su in (st.users or []):
                        if su.is_active and su.user:
                            st_users.append(UserSimple(
                                id=su.user.employee_id,  # или su.user.id — смотрите UserSimple
                                name=su.user.name,
                            ))

                    flat_subtasks.append(SubtaskTree(
                        id=st.id,
                        parent_task_id=task.id,
                        name=st.name,
                        description=st.description,
                        status_id=st.status_id,
                        date_time_start=st.date_time_start,
                        date_time_end=st.date_time_end,
                        users=st_users,
                    ))

        return KanbanBoardResponse(
            board=board_flat,
            columns=flat_columns,
            tasks=flat_tasks,
            subtasks=flat_subtasks,
        )