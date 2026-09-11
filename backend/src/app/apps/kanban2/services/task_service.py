from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.tasks.Task import Task
from ..models.tasks.TaskData import TaskData
from ..models.tasks.TaskUser import TaskUser

from ..schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        query = (
            select(Task)
            .options(
                selectinload(Task.column),
                selectinload(Task.status),
                selectinload(Task.data),
                selectinload(Task.users)
                # SubTask намеренно исключен
            )
            .where(Task.id == task_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_tasks_by_column(self, column_id: int) -> List[Task]:
        query = (
            select(Task)
            .options(
                selectinload(Task.status),
                selectinload(Task.data),
                selectinload(Task.users)
            )
            .where(Task.column_id == column_id, Task.is_active == True)
            .order_by(Task.position.asc(), Task.id.asc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create_task(self, task_data: TaskCreate) -> Task:
        if task_data.position is None:
            max_pos = await self._get_max_position(task_data.column_id)
            task_data.position = (max_pos or 0) + 1
        
        task = Task(
            column_id=task_data.column_id,
            status_id=task_data.status_id,
            name=task_data.name,
            description=task_data.description,
            position=task_data.position,
            date_time_start=task_data.date_time_start,
            date_time_end=task_data.date_time_end,
            planing_date_time_start=task_data.planing_date_time_start,
            planing_date_time_end=task_data.planing_date_time_end,
            is_active=True
        )
        
        self.db.add(task)
        await self.db.flush()
        
        if task_data.data:
            data_obj = TaskData(
                task_id=task.id,
                owner_id=task_data.data.owner_id,
                big_description=task_data.data.big_description
            )
            self.db.add(data_obj)
        
        if task_data.users:
            for u in task_data.users:
                self.db.add(TaskUser(task_id=task.id, user_id=u.user_id, role=u.role))
        
        await self.db.commit()
        await self.db.refresh(task)
        await self.db.refresh(task, ['data', 'users'])
        return task
    
    async def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        task = await self.get_task_by_id(task_id)
        if not task:
            return None
        
        for field in ['name', 'description', 'position', 'column_id', 'status_id', 
                      'date_time_start', 'date_time_end', 'planing_date_time_start', 
                      'planing_date_time_end', 'is_active']:
            val = getattr(task_data, field)
            if val is not None:
                setattr(task, field, val)
        
        if task_data.data:
            if task.data:
                if task_data.data.owner_id: task.data.owner_id = task_data.data.owner_id
                if task_data.data.big_description is not None: task.data.big_description = task_data.data.big_description
            else:
                self.db.add(TaskData(
                    task_id=task.id,
                    owner_id=task_data.data.owner_id,
                    big_description=task_data.data.big_description
                ))
        
        await self.db.commit()
        await self.db.refresh(task)
        await self.db.refresh(task, ['data', 'users'])
        return task
    
    async def reorder_tasks(self, column_id: int, task_ids: List[int]) -> bool:
        for idx, tid in enumerate(task_ids):
            t = await self.get_task_by_id(tid)
            if not t or t.column_id != column_id:
                raise ValueError(f"Task {tid} invalid")
            t.position = idx + 1
        await self.db.commit()
        return True
    
    async def delete_task(self, task_id: int, hard: bool = False) -> bool:
        task = await self.get_task_by_id(task_id)
        if not task: return False
        
        if hard:
            await self.db.delete(task)
        else:
            task.is_active = False
            task.remove_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        return True

    async def _get_max_position(self, column_id: int) -> Optional[int]:
        res = await self.db.execute(select(func.max(Task.position)).where(Task.column_id == column_id))
        return res.scalar()