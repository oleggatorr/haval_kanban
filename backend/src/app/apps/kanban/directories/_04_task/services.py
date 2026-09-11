# src\app\apps\kanban\directories\_04_task\services.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from sqlalchemy.sql import func

from .models import Task, TaskAssignee
from .._03_column.models import Column
from .._03_column.services import ColumnService
# Импортируем модель профиля пользователя (проверьте путь к вашему файлу models.py профиля)
from src.app.apps.kanban.user_profille.profille.profille_models import UserProfile 
from src.app.apps.kanban.user_profille.profille.profille_services import UserService

from .schemas import TaskCreate, TaskUpdate, TaskResponse, AssigneeInfo, Task_deep_Response, TaskMove


class TaskService:
    """Сервис для работы с задачами"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_column_exists(self, column_id: int) -> bool:
        """Проверка существования колонки"""
        result = await self.db.execute(
            select(Column).where(Column.id == column_id)
        )
        return result.scalar_one_or_none() is not None

    async def _validate_employee_ids(self, employee_ids: List[str]) -> List[str]:
        """
        Проверка существования пользователей по employee_id
        
        Args:
            employee_ids: Список ID сотрудников
            
        Returns:
            Список валидных employee_id
            
        Raises:
            ValueError: Если один или несколько сотрудников не найдены
        """
        if not employee_ids:
            return []
        
        user_service = UserService(self.db)
        invalid_ids = []
        
        for emp_id in employee_ids:
            user = await user_service.get_user_by_employee_id(emp_id)
            if not user:
                invalid_ids.append(emp_id)
        
        if invalid_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Сотрудники с ID {invalid_ids} не найдены в системе"
            )
        
        return employee_ids

    async def _get_task_with_assignees(self, task_id: int) -> TaskResponse:
        """
        Вспомогательный метод: получает задачу и собирает список исполнителей.
        """
        # 1. Получаем саму задачу
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise ValueError(f"Задача с ID {task_id} не найдена")

        # 2. Получаем данные исполнителей через JOIN
        assignees_result = await self.db.execute(
            select(UserProfile.display_name, TaskAssignee.employee_id)
            .join(TaskAssignee, UserProfile.employee_id == TaskAssignee.employee_id)
            .where(TaskAssignee.task_id == task_id)
        )
        
        rows = assignees_result.all()
        assignees_list = [
            AssigneeInfo(employee_id=row.employee_id, display_name=row.display_name)
            for row in rows
        ]

        # 3. Формируем ответ
        return TaskResponse(
            id=task.id,
            column_id=task.column_id,
            name=task.name,
            order_id=task.order_id,
            is_complit=task.is_complit,
            assignees=assignees_list
        )

    async def _get_column_tab_id(self, column_id: int) -> Optional[int]:
        """
        Получение tab_id колонки
        
        Args:
            column_id: ID колонки
            
        Returns:
            tab_id или None если колонка не найдена
        """
        result = await self.db.execute(
            select(Column.tab_id).where(Column.id == column_id)
        )
        return result.scalar_one_or_none()

    async def _touch_column(self, column_id: int) -> None:
        """
        Обновление временной метки колонки и связанного таба
        
        Args:
            column_id: ID колонки
        """
        # Получаем tab_id колонки
        tab_id = await self._get_column_tab_id(column_id)
        if tab_id is not None:
            # Обновляем колонку через ColumnService
            column_service = ColumnService(self.db)
            await column_service.touch_column(column_id)
    
    async def _update_assignees(self, task_id: int, employee_ids: List[str]):
        """
        Полная замена списка исполнителей для задачи.
        1. Проверяет существование пользователей.
        2. Удаляет старые связи.
        3. Добавляет новые.
        """
        # Проверяем существование всех сотрудников
        await self._validate_employee_ids(employee_ids)
        
        # Удаляем текущие назначения
        await self.db.execute(
            delete(TaskAssignee).where(TaskAssignee.task_id == task_id)
        )
        
        if employee_ids:
            # Создаем новые связи
            new_assignees = [
                TaskAssignee(task_id=task_id, employee_id=emp_id)
                for emp_id in employee_ids
            ]
            self.db.add_all(new_assignees)

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Создание новой задачи с назначением исполнителей"""
        if not await self._check_column_exists(task_data.column_id):
            raise ValueError(f"Колонка с ID {task_data.column_id} не существует")
        
        db_task = Task(
            column_id=task_data.column_id,
            name=task_data.name,
            order_id=task_data.order_id,
            is_complit=task_data.is_complit
        )
        
        self.db.add(db_task)
        await self.db.flush()  # Получаем ID задачи в БД
        
        # Назначаем исполнителей, если они переданы
        if task_data.assignee_ids:
            await self._update_assignees(db_task.id, task_data.assignee_ids)
            
        await self.db.commit()
        
        # Нормализуем порядки и обновляем колонку
        await self.normalize_task_orders(task_data.column_id)
        await self._touch_column(task_data.column_id)
        
        # Возвращаем задачу с полными данными об исполнителях
        return await self._get_task_with_assignees(db_task.id)

    async def get_task_by_id(self, task_id: int) -> Optional[TaskResponse]:
        """Получение задачи по ID с исполнителями"""
        try:
            return await self._get_task_with_assignees(task_id)
        except ValueError:
            return None
        
    async def get_task_by_id_deep(self, task_id: int) -> Optional[Task_deep_Response]:
        """Получение задачи по ID с исполнителями и подзадачами"""
        try:
            # 1. Получаем задачу с исполнителями
            task_response = await self.get_task_by_id(task_id)
            
            if not task_response:
                return None
            
            # 2. Получаем подзадачи
            from .._05_sub_task.services import SubTaskService
            subtaskservices = SubTaskService(self.db)
            
            sab_tasks = await subtaskservices.get_sub_tasks_by_task_id(task_id)
            
            # Преобразуем подзадачи в схемы
            subtasks_list = sab_tasks
            
            # 3. Создаем Task_deep_Response
            task_dict = task_response.model_dump()
            task_dict['subtasks'] = subtasks_list
            
            task_deep = Task_deep_Response.model_validate(task_dict)
            
            return task_deep
            
        except ValueError:
            return None
    
    async def get_task_by_column_deep(self, column_id: int) -> List[Task_deep_Response]:
        """Получение всех задач колонки с исполнителями и подзадачами"""
        try:
            # 1. Получаем все задачи колонки с исполнителями
            tasks_response = await self.get_tasks_by_column_id(column_id)
            
            if not tasks_response:
                return []
            
            # 2. Импортируем сервис подзадач
            from .._05_sub_task.services import SubTaskService
            subtask_service = SubTaskService(self.db)
            
            # 3. Для каждой задачи получаем подзадачи
            deep_tasks = []
            for task in tasks_response:
                # Получаем подзадачи для текущей задачи
                subtasks = await subtask_service.get_sub_tasks_by_task_id(task.id)
                
                # Преобразуем задачу в словарь и добавляем подзадачи
                task_dict = task.model_dump()
                task_dict['subtasks'] = subtasks  # subtasks уже в формате SubTaskResponse
                
                # Создаем Task_deep_Response
                task_deep = Task_deep_Response.model_validate(task_dict)
                deep_tasks.append(task_deep)
            
            return deep_tasks
            
        except ValueError as e:
            print(f"ValueError in get_task_by_column_deep: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in get_task_by_column_deep: {e}")
            return []
    
    
    async def get_tasks_by_column_id(self, column_id: int) -> List[TaskResponse]:
        """Получение всех задач колонки с исполнителями"""
        if not await self._check_column_exists(column_id):
            raise ValueError(f"Колонка с ID {column_id} не существует")
        
        result = await self.db.execute(
            select(Task)
            .where(Task.column_id == column_id)
            .order_by(Task.order_id)
        )
        tasks = result.scalars().all()
        
        # Для каждой задачи подгружаем исполнителей
        # Примечание: В продакшене лучше сделать один запрос с JOIN для всех задач, 
        # но для простоты оставим по одному запросу на задачу или используем _get_task_with_assignees
        response_list = []
        for task in tasks:
            response_list.append(await self._get_task_with_assignees(task.id))
            
        return response_list

    async def get_all_tasks(self) -> List[TaskResponse]:
        """Получение всех задач"""
        result = await self.db.execute(select(Task))
        tasks = result.scalars().all()
        
        response_list = []
        for task in tasks:
            response_list.append(await self._get_task_with_assignees(task.id))
        return response_list

    async def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[TaskResponse]:
        """Обновление задачи и её исполнителей"""
        # Проверяем существование задачи через вспомогательный метод (он выбросит ошибку если нет)
        try:
            # Сначала просто проверим наличие, чтобы вернуть None если нет
            check_res = await self.db.execute(select(Task.id).where(Task.id == task_id))
            if not check_res.scalar_one_or_none():
                return None
        except:
            return None

        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one()
        
        column_id = task.column_id
        
        # Обновляем поля задачи
        if task_data.name is not None:
            task.name = task_data.name
        if task_data.order_id is not None:
            task.order_id = task_data.order_id
        if task_data.is_complit is not None:
            task.is_complit = task_data.is_complit
        
        # Обновляем исполнителей, если поле было передано (даже если пустой список)
        if task_data.assignee_ids is not None:
            await self._update_assignees(task_id, task_data.assignee_ids)
        
        await self.db.commit()
        
        # Обновляем колонку
        await self._touch_column(column_id)
        
        return await self._get_task_with_assignees(task_id)

    async def delete_task(self, task_id: int) -> bool:
        """Удаление задачи (связи удалятся каскадом)"""
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            return False
        
        column_id = task.column_id
        
        await self.db.delete(task)
        await self.db.commit()
        
        # Нормализуем порядки и обновляем колонку
        await self.normalize_task_orders(column_id)
        await self._touch_column(column_id)
        
        return True

    async def normalize_task_orders(self, column_id: int) -> List[TaskResponse]:
        """Нормализация порядков задач в колонке"""
        if not await self._check_column_exists(column_id):
            raise ValueError(f"Колонка с ID {column_id} не существует")
        
        result = await self.db.execute(
            select(Task)
            .where(Task.column_id == column_id)
            .order_by(Task.order_id, Task.id)
        )
        tasks = result.scalars().all()
        
        for index, task in enumerate(tasks, start=1):
            task.order_id = index
        
        await self.db.commit()
        
        # Обновляем колонку
        await self._touch_column(column_id)
        
        # Возвращаем обновленный список с исполнителями
        return [await self._get_task_with_assignees(t.id) for t in tasks]

    async def reorder_tasks(self, column_id: int, new_order: List[int]) -> List[TaskResponse]:
        """Изменение порядка задач в колонке"""
        if not await self._check_column_exists(column_id):
            raise ValueError(f"Колонка с ID {column_id} не существует")
        
        if not new_order:
            raise ValueError("Список ID задач не может быть пустым")
        
        result = await self.db.execute(select(Task).where(Task.column_id == column_id))
        existing_tasks = result.scalars().all()
        existing_task_ids = {task.id for task in existing_tasks}
        
        new_order_set = set(new_order)
        if not new_order_set.issubset(existing_task_ids):
            invalid_ids = new_order_set - existing_task_ids
            raise ValueError(f"Задачи с ID {invalid_ids} не принадлежат колонке {column_id}")
        
        if len(new_order) != len(existing_tasks):
            raise ValueError(
                f"Количество ID в списке ({len(new_order)}) не совпадает "
                f"с количеством задач в колонке ({len(existing_tasks)})"
            )
        
        for index, task_id in enumerate(new_order, start=1):
            task = next((t for t in existing_tasks if t.id == task_id), None)
            if task:
                task.order_id = index
        
        await self.db.commit()
        
        # Обновляем колонку
        await self._touch_column(column_id)
        
        result = await self.db.execute(
            select(Task)
            .where(Task.column_id == column_id)
            .order_by(Task.order_id)
        )
        reordered_tasks = result.scalars().all()
        
        return [await self._get_task_with_assignees(t.id) for t in reordered_tasks]

    # ============ МЕТОДЫ ДЛЯ "КАСАНИЯ" ============

    async def touch_task(self, task_id: int) -> Optional[TaskResponse]:
        """
        Обновление только поля updated_at задачи и связанной колонки
        
        Используется для обновления временной метки без изменения данных.
        
        Args:
            task_id: ID задачи
            
        Returns:
            Обновленная задача или None если не найдена
        """
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            return None
        
        column_id = task.column_id
        
        # Принудительно обновляем updated_at задачи
        task.updated_at = func.now()
        
        await self.db.commit()
        await self.db.refresh(task)
        
        # Обновляем колонку
        await self._touch_column(column_id)
        
        return await self._get_task_with_assignees(task_id)

    async def touch_tasks_by_column(self, column_id: int) -> List[TaskResponse]:
        """
        Обновление поля updated_at для всех задач колонки
        
        Args:
            column_id: ID колонки
            
        Returns:
            Список обновленных задач
            
        Raises:
            ValueError: Если колонка не существует
        """
        if not await self._check_column_exists(column_id):
            raise ValueError(f"Колонка с ID {column_id} не существует")
        
        # Получаем все задачи колонки
        result = await self.db.execute(
            select(Task).where(Task.column_id == column_id)
        )
        tasks = result.scalars().all()
        
        if not tasks:
            return []
        
        # Обновляем updated_at для всех задач
        now = func.now()
        for task in tasks:
            task.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for task in tasks:
            await self.db.refresh(task)
        
        # Обновляем колонку
        await self._touch_column(column_id)
        
        return [await self._get_task_with_assignees(task.id) for task in tasks]

    async def bulk_touch_tasks(self, task_ids: List[int]) -> List[TaskResponse]:
        """
        Массовое обновление поля updated_at для нескольких задач
        
        Args:
            task_ids: Список ID задач
            
        Returns:
            Список обновленных задач
        """
        if not task_ids:
            return []
        
        # Получаем все задачи по списку ID
        result = await self.db.execute(
            select(Task).where(Task.id.in_(task_ids))
        )
        tasks = result.scalars().all()
        
        if not tasks:
            return []
        
        # Сохраняем уникальные column_id для обновления
        column_ids = {task.column_id for task in tasks}
        
        # Обновляем updated_at для всех найденных задач
        now = func.now()
        for task in tasks:
            task.updated_at = now
        
        await self.db.commit()
        
        # Обновляем объекты из БД
        for task in tasks:
            await self.db.refresh(task)
        
        # Обновляем все затронутые колонки
        for column_id in column_ids:
            await self._touch_column(column_id)
        
        return [await self._get_task_with_assignees(task.id) for task in tasks]
    
    
    async def move_task_to_column(self, task_id: int, new_column: TaskMove) -> Optional[TaskResponse]:
        """
        Перенос задачи в другую колонку
        
        Args:
            task_id: ID задачи
            new_column_id: ID новой колонки
            
        Returns:
            Обновленная задача или None если задача не найдена
            
        Raises:
            ValueError: Если новая колонка не существует
        """
        new_column_id = new_column.new_column_id
        
        # Проверяем существование новой колонки
        if not await self._check_column_exists(new_column_id):
            raise ValueError(f"Колонка с ID {new_column_id} не существует")
        
        # Получаем задачу
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            return None
        
        old_column_id = task.column_id
        
        # Если задача уже в нужной колонке, просто возвращаем её
        if task.column_id == new_column_id:
            return await self._get_task_with_assignees(task_id)
        
        # Меняем колонку задачи
        task.column_id = new_column_id
        
        # Сбрасываем order_id - будет нормализован позже
        task.order_id = None
        
        await self.db.commit()
        
        # Нормализуем порядки в старой и новой колонках
        await self.normalize_task_orders(old_column_id)
        await self.normalize_task_orders(new_column_id)
        
        # Обновляем обе колонки
        await self._touch_column(old_column_id)
        await self._touch_column(new_column_id)
        
        return await self._get_task_with_assignees(task_id)