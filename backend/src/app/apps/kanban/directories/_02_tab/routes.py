from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.database.connection import get_db
from .schemas import TabCreate, TabUpdate, TabResponse, ReorderTabsRequest, Tab_deep_Response
from .services import TabService

router = APIRouter(

)


def get_tab_service(db: AsyncSession = Depends(get_db)) -> TabService:
    """Dependency для получения сервиса табов"""
    return TabService(db)


@router.post(
    "/",
    response_model=TabResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый таб",
    description="Создает новый таб в указанном проекте"
)
async def create_tab(
    tab_data: TabCreate,
    service: TabService = Depends(get_tab_service)
):
    """Создание нового таба"""
    try:
        return await service.create_tab(tab_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[TabResponse],
    summary="Получить все табы",
    description="Возвращает список всех табов"
)
async def get_all_tabs(
    service: TabService = Depends(get_tab_service)
):
    """Получение списка всех табов"""
    return await service.get_all_tabs()


@router.get(
    "/project/{project_id}",
    response_model=list[TabResponse],
    summary="Получить табы проекта",
    description="Возвращает список табов указанного проекта, отсортированных по order_id"
)
async def get_tabs_by_project(
    project_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Получение табов по ID проекта"""
    try:
        return await service.get_tabs_by_project_id(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{tab_id}",
    response_model=TabResponse,
    summary="Получить таб по ID",
    description="Возвращает таб по его идентификатору"
)
async def get_tab(
    tab_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Получение таба по ID"""
    tab = await service.get_tab_by_id(tab_id)
    
    if not tab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Таб с ID {tab_id} не найден"
        )
    
    return tab


@router.put(
    "/{tab_id}",
    response_model=TabResponse,
    summary="Обновить таб",
    description="Обновляет данные существующего таба"
)
async def update_tab(
    tab_id: int,
    tab_data: TabUpdate,
    service: TabService = Depends(get_tab_service)
):
    """Обновление таба"""
    updated_tab = await service.update_tab(tab_id, tab_data)
    
    if not updated_tab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Таб с ID {tab_id} не найден"
        )
    
    return updated_tab


@router.delete(
    "/{tab_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить таб",
    description="Удаляет таб и все связанные с ним колонки (cascade)"
)
async def delete_tab(
    tab_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Удаление таба"""
    deleted = await service.delete_tab(tab_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Таб с ID {tab_id} не найден"
        )
    
    return None


@router.get(
    "/{tab_id}/deep",
    response_model=Tab_deep_Response,
    summary="Получить таб с глубокими данными",
    description="Возвращает таб с колонками, задачами, подзадачами и исполнителями"
)
async def get_tab_deep(
    tab_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Получение таба с глубокими данными"""
    tab = await service.get_tab_by_id_deep(tab_id)
    
    if not tab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Таб с ID {tab_id} не найден"
        )
    
    return tab

@router.get(
    "/project/{project_id}",
    response_model=List[TabResponse],
    summary="Получить табы проекта",
    description="Возвращает список табов указанного проекта, отсортированных по order_id"
)
async def get_tabs_by_project(
    project_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Получение табов по ID проекта"""
    try:
        return await service.get_tabs_by_project_id(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get(
    "/project/{project_id}/deep",
    response_model=List[Tab_deep_Response],
    summary="Получить табы проекта с глубокими данными",
    description="Возвращает все табы проекта с колонками, задачами, подзадачами и исполнителями"
)
async def get_tabs_by_project_deep(
    project_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Получение всех табов проекта с глубокими данными"""
    try:
        return await service.get_tabs_by_project_id_deep(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    "/project/{project_id}/normalize-orders",
    response_model=list[TabResponse],
    summary="Нормализовать порядки табов",
    description="Переназначает order_id всем табам проекта последовательно от 1 до N"
)
async def normalize_tab_orders(
    project_id: int,
    service: TabService = Depends(get_tab_service)
):
    """Нормализация порядков табов в проекте"""
    try:
        return await service.normalize_tab_orders(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/project/{project_id}/reorder",
    response_model=list[TabResponse],
    summary="Изменить порядок табов",
    description="Изменяет порядок табов согласно переданному списку ID"
)
async def reorder_tabs(
    project_id: int,
    new_order: List[int],
    service: TabService = Depends(get_tab_service)
):
    """Изменение порядка табов в проекте"""
    try:
        return await service.reorder_tabs(project_id, new_order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )