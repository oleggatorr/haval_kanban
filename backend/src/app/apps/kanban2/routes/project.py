from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from ..schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse
)
from ..services.project_service import ProjectService
from ..services.board_tree_service import KanbanService
from ..schemas.tree import *


router = APIRouter()


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    """Dependency для получения сервиса проектов."""
    return ProjectService(db)


@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
    is_active: bool | None = Query(None, description="Фильтр по активности"),
    service: ProjectService = Depends(get_project_service)
):
    """Получить список проектов с пагинацией."""
    
    projects, total = await service.get_projects(
        page=page,
        page_size=page_size,
        is_active=is_active
    )
    
    return ProjectListResponse(
        items=[ProjectResponse.model_validate(p) for p in projects],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Получить проект по ID."""
    
    project = await service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    return ProjectResponse.model_validate(project)


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """Создать новый проект."""
    
    try:
        project = await service.create_project(project_data)
        return ProjectResponse.model_validate(project)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания проекта: {str(e)}")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """Обновить проект."""
    
    project = await service.update_project(project_id, project_data)
    
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    return ProjectResponse.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def patch_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """Частично обновить проект."""
    
    project = await service.update_project(project_id, project_data)
    
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    hard: bool = Query(False, description="Полное удаление (true) или мягкое (false)"),
    service: ProjectService = Depends(get_project_service)
):
    """Удалить проект."""
    
    if hard:
        success = await service.hard_delete_project(project_id)
    else:
        success = await service.delete_project(project_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    return {"message": "Проект успешно удален"}


@router.get("/{project_id}/full-board")
async def get_project_full_board(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить полную структуру доски проекта в виде дерева.
    Включает: Проект -> Доска -> Колонки -> Задачи (с данными и пользователями).
    """
    service = KanbanService(db)
    tree = await service.get_kanban_data(project_id)
    
    if not tree:
        raise HTTPException(status_code=404, detail="Проект или его доска не найдены")
        
    return tree