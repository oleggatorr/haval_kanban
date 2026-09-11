from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from ..schemas.task_column import (
    TaskColumnCreate,
    TaskColumnUpdate,
    TaskColumnResponse,
    TaskColumnListResponse,
    TaskColumnReorderRequest
)
from ..services.task_column_service import TaskColumnService

router = APIRouter()


def get_task_column_service(db: AsyncSession = Depends(get_db)) -> TaskColumnService:
    """Dependency для получения сервиса колонок."""
    return TaskColumnService(db)


@router.get("/", response_model=TaskColumnListResponse)
async def get_columns(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Элементов на странице"),
    board_id: int | None = Query(None, description="Фильтр по доске"),
    is_active: bool | None = Query(None, description="Фильтр по активности"),
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Получить список колонок с пагинацией."""
    
    columns, total = await service.get_columns_paginated(
        page=page,
        page_size=page_size,
        board_id=board_id,
        is_active=is_active
    )
    
    return TaskColumnListResponse(
        items=[TaskColumnResponse.model_validate(c) for c in columns],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/by-board/{board_id}", response_model=list[TaskColumnResponse])
async def get_columns_by_board(
    board_id: int,
    is_active: bool | None = Query(None, description="Фильтр по активности"),
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Получить все колонки доски, отсортированные по позиции."""
    
    columns = await service.get_columns_by_board(board_id, is_active)
    
    return [TaskColumnResponse.model_validate(c) for c in columns]


@router.get("/{column_id}", response_model=TaskColumnResponse)
async def get_column(
    column_id: int,
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Получить колонку по ID."""
    
    column = await service.get_column_by_id(column_id)
    
    if not column:
        raise HTTPException(status_code=404, detail="Колонка не найдена")
    
    return TaskColumnResponse.model_validate(column)


@router.post("/", response_model=TaskColumnResponse, status_code=201)
async def create_column(
    column_data: TaskColumnCreate,
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Создать новую колонку на доске."""
    
    try:
        column = await service.create_column(column_data)
        return TaskColumnResponse.model_validate(column)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания колонки: {str(e)}")


@router.patch("/{column_id}", response_model=TaskColumnResponse)
async def patch_column(
    column_id: int,
    column_data: TaskColumnUpdate,
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Частично обновить колонку."""
    
    column = await service.update_column(column_id, column_data)
    
    if not column:
        raise HTTPException(status_code=404, detail="Колонка не найдена")
    
    return TaskColumnResponse.model_validate(column)


@router.post("/reorder")
async def reorder_columns(
    reorder_data: TaskColumnReorderRequest,
    board_id: int = Query(..., description="ID доски задач"),
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Изменить порядок колонок на доске (drag & drop)."""
    
    try:
        success = await service.reorder_columns(board_id, reorder_data.column_ids)
        
        if not success:
            raise HTTPException(status_code=404, detail="Не удалось изменить порядок")
        
        return {"message": "Порядок колонок успешно обновлен"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при изменении порядка: {str(e)}")


@router.delete("/{column_id}")
async def delete_column(
    column_id: int,
    hard: bool = Query(False, description="Полное удаление (true) или мягкое (false)"),
    service: TaskColumnService = Depends(get_task_column_service)
):
    """Удалить колонку."""
    
    if hard:
        success = await service.hard_delete_column(column_id)
    else:
        success = await service.delete_column(column_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Колонка не найдена")
    
    return {"message": "Колонка успешно удалена"}