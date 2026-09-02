from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Employee
from .schemas import EmployeeResponse
import logging


logger = logging.getLogger(__name__)

def normalise_employee_id(employee_id: str):
    """Нормализация employee_id к ЗУП состоянию"""
    employee_id.lower()
    if employee_id[:5] == "gw070":
        employee_id = '0' * 5 + employee_id[5:]
    return employee_id

class EmployeeService:
    """Сервис для работы с сотрудниками (только чтение)"""
    
    

    
    @staticmethod
    async def get_all_employees(
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0
    ) -> list[EmployeeResponse]:
        """
        Получить список всех сотрудников с пагинацией
        
        Args:
            session: Асинхронная сессия БД
            limit: Количество записей
            offset: Смещение
            
        Returns:
            Список сотрудников
        """
        try:
            query = (
                select(Employee)
                .order_by(Employee.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            employees = result.scalars().all()
            
            return [EmployeeResponse.model_validate(emp) for emp in employees]
        except Exception as e:
            logger.error(f"Ошибка получения списка сотрудников: {e}")
            raise
    
    @staticmethod
    async def get_employee_by_guid(
        session: AsyncSession,
        guid: str
    ) -> EmployeeResponse | None:
        """
        Получить сотрудника по GUID
        
        Args:
            session: Асинхронная сессия БД
            guid: GUID сотрудника
            
        Returns:
            Сотрудник или None
        """
        try:
            query = select(Employee).where(Employee.guid == guid)
            result = await session.execute(query)
            employee = result.scalar_one_or_none()
            
            if employee:
                return EmployeeResponse.model_validate(employee)
            return None
        except Exception as e:
            logger.error(f"Ошибка получения сотрудника по GUID {guid}: {e}")
            raise
    
    @staticmethod
    async def get_employee_by_id(
        session: AsyncSession,
        employee_id: str
    ) -> EmployeeResponse | None:
        employee_id = normalise_employee_id(employee_id)
        """
        Получить сотрудника по employee_id
        
        Args:
            session: Асинхронная сессия БД
            employee_id: ID сотрудника
            
        Returns:
            Сотрудник или None
        """
        try:
            query = select(Employee).where(Employee.employee_id == employee_id)
            result = await session.execute(query)
            employee = result.scalar_one_or_none()
            
            if employee:
                return EmployeeResponse.model_validate(employee)
            return None
        except Exception as e:
            logger.error(f"Ошибка получения сотрудника по ID {employee_id}: {e}")
            raise
    
    @staticmethod
    async def search_employees(
        session: AsyncSession,
        search_term: str,
        limit: int = 50
    ) -> list[EmployeeResponse]:
        """
        Поиск сотрудников по ФИО
        
        Args:
            session: Асинхронная сессия БД
            search_term: Поисковый запрос
            limit: Количество результатов
            
        Returns:
            Список найденных сотрудников
        """
        try:
            search_pattern = f"%{search_term}%"
            query = (
                select(Employee)
                .where(
                    (Employee.last_name.ilike(search_pattern)) |
                    (Employee.first_name.ilike(search_pattern)) |
                    (Employee.middle_name.ilike(search_pattern)) |
                    (Employee.employee_id.ilike(search_pattern))
                )
                .order_by(Employee.last_name)
                .limit(limit)
            )
            result = await session.execute(query)
            employees = result.scalars().all()
            
            return [EmployeeResponse.model_validate(emp) for emp in employees]
        except Exception as e:
            logger.error(f"Ошибка поиска сотрудников: {e}")
            raise
    
    @staticmethod
    async def get_employees_count(session: AsyncSession) -> int:
        """
        Получить общее количество сотрудников
        
        Args:
            session: Асинхронная сессия БД
            
        Returns:
            Количество сотрудников
        """
        try:
            query = select(func.count()).select_from(Employee)
            result = await session.execute(query)
            return result.scalar()
        except Exception as e:
            logger.error(f"Ошибка получения количества сотрудников: {e}")
            raise