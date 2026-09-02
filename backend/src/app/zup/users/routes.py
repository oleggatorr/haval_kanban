from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.zup_connection import get_db
from .services import EmployeeService
from .schemas import EmployeeResponse
from typing import Optional

router = APIRouter()


@router.get("/", response_model=list[EmployeeResponse])
async def get_employees(
    limit: int = Query(default=100, ge=1, le=1000, description="Количество записей"),
    offset: int = Query(default=0, ge=0, description="Смещение"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список сотрудников с пагинацией
    """
    try:
        employees = await EmployeeService.get_all_employees(
            session=db,
            limit=limit,
            offset=offset
        )
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {str(e)}")


@router.get("/count")
async def get_employees_count(db: AsyncSession = Depends(get_db)):
    """
    Получить общее количество сотрудников
    """
    try:
        count = await EmployeeService.get_employees_count(session=db)
        return {"total": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


@router.get("/{guid}", response_model=EmployeeResponse)
async def get_employee_by_guid(
    guid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить сотрудника по GUID
    """
    try:
        employee = await EmployeeService.get_employee_by_guid(
            session=db,
            guid=guid
        )
        
        if not employee:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")
        
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


@router.get("/id/{employee_id}", response_model=EmployeeResponse)
async def get_employee_by_id(
    employee_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить сотрудника по employee_id
    """
    try:
        employee = await EmployeeService.get_employee_by_id(
            session=db,
            employee_id=employee_id
        )
        
        if not employee:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")
        
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


@router.get("/search/", response_model=list[EmployeeResponse])
async def search_employees(
    q: str = Query(..., min_length=1, description="Поисковый запрос"),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Поиск сотрудников по ФИО или ID
    """
    try:
        employees = await EmployeeService.search_employees(
            session=db,
            search_term=q,
            limit=limit
        )
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")