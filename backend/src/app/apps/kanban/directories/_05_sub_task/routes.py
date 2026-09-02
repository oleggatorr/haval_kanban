from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.core.database.connection import get_db
from .schemas import SubTaskCreate, SubTaskUpdate, SubTaskResponse
from .services import SubTaskService

router = APIRouter(
)


def get_sub_task_service(db: AsyncSession = Depends(get_db)) -> SubTaskService:
    """Dependency для получения сервиса подзадач"""
    return SubTaskService(db)


# =============================================================================
# Базовые CRUD эндпоинты
# =============================================================================

@router.post(
    "/",
    response_model=SubTaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую подзадачу",
    description="Создает новую подзадачу для указанной задачи"
)
async def create_sub_task(
    sub_task_data: SubTaskCreate,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Создание новой подзадачи"""
    try:
        return await service.create_sub_task(sub_task_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[SubTaskResponse],
    summary="Получить все подзадачи",
    description="Возвращает список всех подзадач с возможностью фильтрации по задаче"
)
async def get_all_sub_tasks(
    task_id: Optional[int] = Query(None, description="ID задачи для фильтрации подзадач"),
    service: SubTaskService = Depends(get_sub_task_service)
):
    """
    Получение списка всех подзадач.
    Если указан task_id, возвращает подзадачи только этой задачи.
    """
    if task_id is not None:
        try:
            return await service.get_sub_tasks_by_task_id(task_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    return await service.get_all_sub_tasks()


@router.get(
    "/task/{task_id}",
    response_model=List[SubTaskResponse],
    summary="Получить подзадачи задачи",
    description="Возвращает список подзадач указанной задачи"
)
async def get_sub_tasks_by_task(
    task_id: int,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Получение подзадач по ID задачи"""
    try:
        return await service.get_sub_tasks_by_task_id(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{sub_task_id}",
    response_model=SubTaskResponse,
    summary="Получить подзадачу по ID",
    description="Возвращает подзадачу по ее идентификатору"
)
async def get_sub_task(
    sub_task_id: int,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Получение подзадачи по ID"""
    sub_task = await service.get_sub_task_by_id(sub_task_id)
    
    if not sub_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подзадача с ID {sub_task_id} не найдена"
        )
    
    return sub_task


@router.put(
    "/{sub_task_id}",
    response_model=SubTaskResponse,
    summary="Обновить подзадачу",
    description="Обновляет данные существующей подзадачи"
)
async def update_sub_task(
    sub_task_id: int,
    sub_task_data: SubTaskUpdate,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Обновление подзадачи"""
    try:
        updated_sub_task = await service.update_sub_task(sub_task_id, sub_task_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    if not updated_sub_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подзадача с ID {sub_task_id} не найдена"
        )
    
    return updated_sub_task


@router.delete(
    "/{sub_task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить подзадачу",
    description="Удаляет подзадачу"
)
async def delete_sub_task(
    sub_task_id: int,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Удаление подзадачи"""
    deleted = await service.delete_sub_task(sub_task_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подзадача с ID {sub_task_id} не найдена"
        )
    
    return None


# =============================================================================
# Дополнительные эндпоинты для управления порядком
# =============================================================================

@router.post(
    "/task/{task_id}/normalize",
    response_model=List[SubTaskResponse],
    summary="Нормализовать порядок подзадач",
    description="Перенумеровывает order_id подзадач задачи от 1 до N"
)
async def normalize_sub_task_orders(
    task_id: int,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Нормализация порядковых номеров подзадач"""
    try:
        return await service.normalize_sub_task_orders(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/task/{task_id}/reorder",
    response_model=List[SubTaskResponse],
    summary="Изменить порядок подзадач",
    description="Обновляет порядок подзадач согласно переданному списку ID"
)
async def reorder_sub_tasks(
    task_id: int,
    new_order: List[int],
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Изменение порядка подзадач"""
    try:
        return await service.reorder_sub_tasks(task_id, new_order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/task/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить все подзадачи задачи",
    description="Удаляет все подзадачи указанной задачи"
)
async def delete_all_sub_tasks_by_task(
    task_id: int,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Удаление всех подзадач задачи"""
    try:
        deleted_count = await service.delete_sub_tasks_by_task_id(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    return None


@router.get(
    "/task/{task_id}/count",
    response_model=int,
    summary="Получить количество подзадач задачи",
    description="Возвращает количество подзадач у указанной задачи"
)
async def get_sub_task_count(
    task_id: int,
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Получение количества подзадач задачи"""
    try:
        return await service.get_sub_task_count_by_task_id(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# =============================================================================
# Пакетные операции
# =============================================================================

@router.post(
    "/batch",
    response_model=List[SubTaskResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Создать несколько подзадач",
    description="Создает несколько подзадач для указанной задачи"
)
async def create_batch_sub_tasks(
    sub_tasks_data: List[SubTaskCreate],
    service: SubTaskService = Depends(get_sub_task_service)
):
    """Массовое создание подзадач"""
    created_tasks = []
    errors = []
    
    for idx, data in enumerate(sub_tasks_data):
        try:
            result = await service.create_sub_task(data)
            created_tasks.append(result)
        except ValueError as e:
            errors.append(f"Ошибка при создании подзадачи #{idx + 1}: {str(e)}")
    
    if errors and not created_tasks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="; ".join(errors)
        )
    
    return created_tasks