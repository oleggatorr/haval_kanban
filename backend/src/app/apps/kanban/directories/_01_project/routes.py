from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse, Project_deep_Response
from .services import ProjectService

router = APIRouter(
)


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    """Dependency для получения сервиса проектов"""
    return ProjectService(db)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый проект",
    description="Создает новый проект с указанными параметрами"
)
async def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """Создание нового проекта"""
    return await service.create_project(project_data)


@router.get(
    "/",
    response_model=list[ProjectResponse],
    summary="Получить все проекты",
    description="Возвращает список всех проектов"
)
async def get_all_projects(
    service: ProjectService = Depends(get_project_service)
):
    """Получение списка всех проектов"""
    return await service.get_all_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Получить проект по ID",
    description="Возвращает проект по его идентификатору"
)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Получение проекта по ID"""
    project = await service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден"
        )
    
    return project


@router.get(
    "/check_update/{project_id}",
    # response_model=ProjectResponse,
    summary="",
    description=""
)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Получение проекта по ID"""
    data = await service.get_project_updated_at(project_id)
    
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден"
        )
    
    return data

@router.get(
    "/{project_id}/deep",
    response_model=Project_deep_Response,
    summary="",
    description=""
)
async def get_project_deep(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Получение проекта по ID"""
    data = await service.get_project_by_id_deep(project_id)
    
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден"
        )
    
    return data

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Обновить проект",
    description="Обновляет данные существующего проекта"
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """Обновление проекта"""
    updated_project = await service.update_project(project_id, project_data)
    
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден"
        )
    
    return updated_project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить проект",
    description="Удаляет проект и все связанные с ним табы (cascade)"
)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Удаление проекта"""
    deleted = await service.delete_project(project_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект с ID {project_id} не найден"
        )
    
    return None