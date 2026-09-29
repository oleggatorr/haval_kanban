from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from ...services.tasks.task_status_service import TaskStatusService
from ...schemas.tasks.task_status import (
    TaskStatusCreate,
    TaskStatusUpdate,
    TaskStatusResponse,
    TaskStatusListResponse,
    TaskStatusSimpleResponse,
    TaskStatusAllResponse
)

router = APIRouter(
    # prefix="/task-statuses",
    # tags=["Task Statuses"],
    responses={404: {"description": "Not found"}}
)


def get_task_status_service(db: AsyncSession = Depends(get_db)) -> TaskStatusService:
    """Dependency для получения сервиса статусов задач."""
    return TaskStatusService(db)


@router.get("/", response_model=TaskStatusListResponse)
async def get_all_statuses(
    skip: int = Query(0, ge=0, description="Пропустить N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей"),
    active_only: bool = Query(False, description="Только активные статусы"),
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Получить список всех статусов задач."""
    
    try:
        statuses, total = await service.get_all(
            skip=skip,
            limit=limit,
            active_only=active_only
        )
        
        return TaskStatusListResponse(
            items=[TaskStatusResponse.model_validate(s) for s in statuses],
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статусов: {str(e)}")


@router.get("/{status_id}", response_model=TaskStatusResponse)
async def get_status_by_id(
    status_id: int,
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Получить статус задачи по ID."""
    
    status = await service.get_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Статус с ID {status_id} не найден")
    
    return TaskStatusResponse.model_validate(status)


@router.post("/", response_model=TaskStatusResponse, status_code=201)
async def create_status(
    status_data: TaskStatusCreate,
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Создать новый статус задачи."""
    
    try:
        new_status = await service.create(status_data)
        return TaskStatusResponse.model_validate(new_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании статуса: {str(e)}")


@router.patch("/{status_id}", response_model=TaskStatusResponse)
async def update_status(
    status_id: int,
    status_data: TaskStatusUpdate,
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Обновить статус задачи."""
    
    updated_status = await service.update(status_id, status_data)
    if not updated_status:
        raise HTTPException(status_code=404, detail=f"Статус с ID {status_id} не найден")
    
    return TaskStatusResponse.model_validate(updated_status)


@router.delete("/{status_id}")
async def delete_status(
    status_id: int,
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Мягко удалить статус задачи."""
    
    success = await service.delete(status_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Статус с ID {status_id} не найден")
    
    return {"message": f"Статус {status_id} успешно удален"}


@router.delete("/{status_id}/hard")
async def hard_delete_status(
    status_id: int,
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Полностью удалить статус задачи."""
    
    success = await service.hard_delete(status_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Статус с ID {status_id} не найден")
    
    return {"message": f"Статус {status_id} полностью удален"}


@router.get("/", response_model=TaskStatusListResponse)
async def get_all_statuses(
    skip: int = Query(0, ge=0, description="Пропустить N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Количество записей"),
    active_only: bool = Query(False, description="Только активные статусы"),
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Получить список всех статусов задач с пагинацией."""
    
    try:
        statuses, total = await service.get_all(
            skip=skip,
            limit=limit,
            active_only=active_only
        )
        
        return TaskStatusListResponse(
            items=[TaskStatusResponse.model_validate(s) for s in statuses],
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статусов: {str(e)}")


@router.get("/all", response_model=TaskStatusAllResponse)
async def get_all_statuses_no_pagination(
    active_only: bool = Query(False, description="Только активные статусы"),
    service: TaskStatusService = Depends(get_task_status_service)
):
    """Получить все статусы задач без пагинации."""
    
    try:
        statuses = await service.get_all_statuses(active_only=active_only)
        
        return TaskStatusAllResponse(
            items=[TaskStatusSimpleResponse.model_validate(s) for s in statuses],
            total=len(statuses)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статусов: {str(e)}")