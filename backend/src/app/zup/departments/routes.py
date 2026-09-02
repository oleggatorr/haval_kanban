from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.zup_connection import get_db
from .services import DepartmentService
from .schemas import DepartmentRead, DepartmentTree
from typing import List

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


def get_department_service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    return DepartmentService(db)


@router.get("/", response_model=List[DepartmentRead])
async def list_departments(service: DepartmentService = Depends(get_department_service)):
    """
    Получить список всех отделов.
    """
    departments = await service.get_all_departments()
    return departments


@router.get("/active", response_model=List[DepartmentRead])
async def list_active_departments(service: DepartmentService = Depends(get_department_service)):
    """
    Получить список активных отделов (без даты закрытия).
    """
    departments = await service.get_active_departments()
    return departments


@router.get("/tree", response_model=List[DepartmentTree])
async def get_department_tree(service: DepartmentService = Depends(get_department_service)):
    """
    Получить иерархическую структуру отделов (дерево).
    """
    tree = await service.build_department_tree()
    return tree


@router.get("/{guid}", response_model=DepartmentRead)
async def get_department(
    guid: str, 
    service: DepartmentService = Depends(get_department_service)
):
    """
    Получить информацию об отделе по его GUID.
    """
    department = await service.get_department_by_guid(guid)
    
    if not department:
        raise HTTPException(status_code=404, detail=f"Department with guid {guid} not found")
    
    return department


@router.get("/search/name", response_model=List[DepartmentRead])
async def search_departments_by_name(
    q: str, 
    service: DepartmentService = Depends(get_department_service)
):
    """Поиск отделов по названию"""
    if not q:
        return []
    return await service.search_by_name(q)

@router.get("/parent/{parent_guid}", response_model=List[DepartmentRead])
async def get_children_by_parent(
    parent_guid: str, 
    service: DepartmentService = Depends(get_department_service)
):
    """Получить дочерние отделы"""
    return await service.get_by_parent_guid(parent_guid)

@router.get("/search/short-name", response_model=List[DepartmentRead])
async def search_by_short_name(
    q: str, 
    service: DepartmentService = Depends(get_department_service)
):
    """Поиск по короткому имени"""
    if not q:
        return []
    return await service.search_by_short_name(q)