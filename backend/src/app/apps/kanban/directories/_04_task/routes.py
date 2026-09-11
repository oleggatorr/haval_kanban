from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.database.connection import get_db
from .schemas import TaskCreate, TaskUpdate, TaskResponse, Task_deep_Response, TaskMove
from .services import TaskService

router = APIRouter(

)


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    """Dependency для получения сервиса задач"""
    return TaskService(db)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу",
    description="Создает новую задачу в указанной колонке"
)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Создание новой задачи"""
    try:
        return await service.create_task(task_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Получить все задачи",
    description="Возвращает список всех задач"
)
async def get_all_tasks(
    service: TaskService = Depends(get_task_service)
):
    """Получение списка всех задач"""
    return await service.get_all_tasks()


@router.get(
    "/column/{column_id}",
    response_model=list[TaskResponse],
    summary="Получить задачи колонки",
    description="Возвращает список задач указанной колонки, отсортированных по order_id"
)
async def get_tasks_by_column(
    column_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Получение задач по ID колонки"""
    try:
        return await service.get_tasks_by_column_id(column_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить задачу по ID",
    description="Возвращает задачу по ее идентификатору"
)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Получение задачи по ID"""
    task = await service.get_task_by_id(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return task


@router.get(
    "/{task_id}/deep",
    response_model=Task_deep_Response,
    summary="Получить задачу по ID",
    description="Возвращает задачу по ее идентификатору"
)
async def get_task_deep(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Получение задачи по ID"""
    task = await service.get_task_by_id_deep(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return task

@router.get(
    "by_column/{column_id}/deep",
    response_model=list[Task_deep_Response],
    summary="",
    description=""
)
async def get_task_deep(
    column_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Получение задачи по ID"""
    task = await service.get_task_by_column_deep(column_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колонка с {column_id} не найдена"
        )
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновить задачу",
    description="Обновляет данные существующей задачи"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Обновление задачи"""
    updated_task = await service.update_task(task_id, task_data)
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет задачу и все связанные с ней подзадачи (cascade)"
)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Удаление задачи"""
    deleted = await service.delete_task(task_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return None


@router.post(
    "/column/{column_id}/normalize-orders",
    response_model=list[TaskResponse],
    summary="Нормализовать порядки задач",
    description="Переназначает order_id всем задачам колонки последовательно от 1 до N"
)
async def normalize_task_orders(
    column_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Нормализация порядков задач в колонке"""
    try:
        return await service.normalize_task_orders(column_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/column/{column_id}/reorder",
    response_model=list[TaskResponse],
    summary="Изменить порядок задач",
    description="Изменяет порядок задач согласно переданному списку ID"
)
async def reorder_tasks(
    column_id: int,
    new_order: List[int],
    service: TaskService = Depends(get_task_service)
):
    """Изменение порядка задач в колонке"""
    try:
        return await service.reorder_tasks(column_id, new_order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{task_id}/move")
async def move_task(
    task_id: int,
    new_column: TaskMove,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    try:
        task = await task_service.move_task_to_column(task_id, new_column)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))