from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.database.connection import get_db
from .schemas import ColumnCreate, ColumnUpdate, ColumnResponse, Column_deep_Response
from .services import ColumnService

router = APIRouter(
)


def get_column_service(db: AsyncSession = Depends(get_db)) -> ColumnService:
    """Dependency для получения сервиса колонок"""
    return ColumnService(db)


@router.post(
    "/",
    response_model=ColumnResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую колонку",
    description="Создает новую колонку в указанном табе"
)
async def create_column(
    column_data: ColumnCreate,
    service: ColumnService = Depends(get_column_service)
):
    """Создание новой колонки"""
    try:
        return await service.create_column(column_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[ColumnResponse],
    summary="Получить все колонки",
    description="Возвращает список всех колонок"
)
async def get_all_columns(
    service: ColumnService = Depends(get_column_service)
):
    """Получение списка всех колонок"""
    return await service.get_all_columns()


@router.get(
    "/tab/{tab_id}",
    response_model=list[ColumnResponse],
    summary="Получить колонки таба",
    description="Возвращает список колонок указанного таба, отсортированных по order_id"
)
async def get_columns_by_tab(
    tab_id: int,
    service: ColumnService = Depends(get_column_service)
):
    """Получение колонок по ID таба"""
    try:
        return await service.get_columns_by_tab_id(tab_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{column_id}",
    response_model=ColumnResponse,
    summary="Получить колонку по ID",
    description="Возвращает колонку по ее идентификатору"
)
async def get_column(
    column_id: int,
    service: ColumnService = Depends(get_column_service)
):
    """Получение колонки по ID"""
    column = await service.get_column_by_id(column_id)
    
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колонка с ID {column_id} не найдена"
        )
    
    return column


@router.put(
    "/{column_id}",
    response_model=ColumnResponse,
    summary="Обновить колонку",
    description="Обновляет данные существующей колонки"
)
async def update_column(
    column_id: int,
    column_data: ColumnUpdate,
    service: ColumnService = Depends(get_column_service)
):
    """Обновление колонки"""
    updated_column = await service.update_column(column_id, column_data)
    
    if not updated_column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колонка с ID {column_id} не найдена"
        )
    
    return updated_column


@router.delete(
    "/{column_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить колонку",
    description="Удаляет колонку и все связанные с ней задачи (cascade)"
)
async def delete_column(
    column_id: int,
    service: ColumnService = Depends(get_column_service)
):
    """Удаление колонки"""
    deleted = await service.delete_column(column_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колонка с ID {column_id} не найдена"
        )
    
    return None


@router.get(
    "/{column_id}/deep",
    response_model=Column_deep_Response,
    summary="",
    description=""
)
async def get_column_deep(
    column_id: int,
    service: ColumnService = Depends(get_column_service)
):
    """Получение колонки по ID"""
    column = await service.get_column_by_id_deep(column_id)
    
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колонка с ID {column_id} не найдена"
        )
    
    return column

@router.get(
    "/by_tab_id/{tab_id}/deep",
    response_model=list[Column_deep_Response],
    summary="",
    description=""
)
async def get_column_deep_by_tab(
    tab_id: int,
    service: ColumnService = Depends(get_column_service)
):
    """Получение колонки по ID"""
    column = await service.get_column_by_tab_id_deep(tab_id)
    
    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"вкладка с ID {tab_id} не найдена"
        )
    
    return column

@router.post(
    "/tab/{tab_id}/normalize-orders",
    response_model=list[ColumnResponse],
    summary="Нормализовать порядки колонок",
    description="Переназначает order_id всем колонкам таба последовательно от 1 до N"
)
async def normalize_column_orders(
    tab_id: int,
    service: ColumnService = Depends(get_column_service)
):
    """Нормализация порядков колонок в табе"""
    try:
        return await service.normalize_column_orders(tab_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/tab/{tab_id}/reorder",
    response_model=list[ColumnResponse],
    summary="Изменить порядок колонок",
    description="Изменяет порядок колонок согласно переданному списку ID"
)
async def reorder_columns(
    tab_id: int,
    new_order: List[int],
    service: ColumnService = Depends(get_column_service)
):
    """Изменение порядка колонок в табе"""
    try:
        return await service.reorder_columns(tab_id, new_order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )