from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.zup_connection import get_db
from .services import EmployeeService
from .schemas import EmployeeResponse


# Типизированные зависимости для переиспользования
AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
EmployeeServiceDep = Annotated[EmployeeService, Depends()]


async def get_employee_by_id(
    session: AsyncSessionDep,
    employee_id: str
) -> EmployeeResponse:
    """
    Зависимость для получения сотрудника по employee_id
    
    Args:
        session: Сессия БД
        employee_id: ID сотрудника
        
    Returns:
        Сотрудник
        
    Raises:
        HTTPException: Если сотрудник не найден
    """
    employee = await EmployeeService.get_employee_by_id(session, employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудник с ID {employee_id} не найден"
        )
    
    return employee
