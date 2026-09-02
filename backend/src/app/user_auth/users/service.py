from uuid import UUID
from typing import Optional, Sequence, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from contextlib import asynccontextmanager

from .models import AuthUser
from .schemas import UserCreate, UserUpdate, UserResponse, UserFullResponse

from ...zup.database.zup_connection import get_db as get_zup_db
from ...zup.users.services import EmployeeService
from ...zup.users.schemas import EmployeeResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    @asynccontextmanager
    async def _get_zup_session():
        """
        Обертка над get_zup_db для использования вне Depends().
        Превращает async-генератор в асинхронный контекстный менеджер.
        """
        gen = get_zup_db()
        session = await gen.__anext__()
        try:
            yield session
        finally:
            try:
                await gen.aclose()
            except StopAsyncIteration:
                pass

    async def zup_get_employee_by_id(self, employee_id: str) -> Optional[EmployeeResponse]:
        """
        Получение сотрудника из внешней БД (ZUP).
        Возвращает словарь с данными сотрудника или None.
        """
        async with self._get_zup_session() as employee_session:
            try:
                employee = await EmployeeService.get_employee_by_id(employee_session, employee_id)
                if employee:
                    return employee
                
                print(f"Сотрудник с ID {employee_id} не найден в ZUP")
                return None
                
            except Exception as e:
                print(f"Ошибка получения сотрудника из ZUP: {e}")
                raise

    # ------------------------------------------------------------------
    # Создание / Обновление
    # ------------------------------------------------------------------

    async def create_user(self, user_in: UserCreate) -> AuthUser:
        """Создание нового пользователя с проверкой существования сотрудника в ZUP."""
        
        # TODO: Проверка существования employee_id
        zup_employee = await self.zup_get_employee_by_id(user_in.employee_id)
        if not zup_employee:
            raise ValueError(
                f"Невозможно создать пользователя: сотрудник с табельным номером "
                f"{user_in.employee_id} не найден в кадровой системе"
            )

        db_user = AuthUser(
            login=user_in.login,
            email=user_in.email,
            employee_id=user_in.employee_id,
            is_active=user_in.is_active,
            password_hash=pwd_context.hash(user_in.password),
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update_user(self, employee_id: str, user_in: UserUpdate) -> Optional[AuthUser]:
        """
        Частичное обновление пользователя.
        Поиск осуществляется по employee_id (табельному номеру).
        """
        # TODO: Поиск по employee_id вместо внутреннего UUID
        db_user = await self.get_user_by_employee_id_raw(employee_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)

        # Отдельная обработка пароля
        if "password" in update_data:
            update_data["password_hash"] = pwd_context.hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    # ------------------------------------------------------------------
    # Публичные методы поиска
    # ------------------------------------------------------------------


    async def get_user_by_login(self, login: str) -> Optional[AuthUser]:
        """Получение пользователя по логину."""
        return await self._get_by_field("login", login)

    async def get_user_by_email(self, email: str) -> Optional[AuthUser]:
        """Получение пользователя по email."""
        return await self._get_by_field("email", email)

    async def get_user_by_employee_id_raw(self, employee_id: str) -> Optional[AuthUser]:
        """Получение модели AuthUser по табельному номеру (без обогащения из ZUP)."""
        return await self._get_by_field("employee_id", employee_id)

    async def get_user_by_employee_id(self, employee_id: str) -> Optional[UserResponse]:
        """Получение базовой информации о пользователе (без данных из ZUP)."""
        db_user = await self.get_user_by_employee_id_raw(employee_id)
        if not db_user:
            return None

        return UserResponse.model_validate(db_user)

    async def get_all_users(self) -> Sequence[AuthUser]:
        """Получение списка всех пользователей, отсортированных по дате создания."""
        stmt = select(AuthUser).order_by(AuthUser.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    
    async def get_full_info(self, employee_id: str) -> Optional[UserFullResponse]:
        """Выдача полной информации о пользователе с данными из ZUP."""
        user_response = await self.get_user_by_employee_id(employee_id)
        if not user_response:
            return None

        zup_data = await self.zup_get_employee_by_id(employee_id)

        return UserFullResponse(
            **user_response.model_dump(),
            zup_info=zup_data,
            warning="Сотрудник не найден в кадровой системе (возможно, уволен)"
                if not zup_data else None,
        )
        

    # ------------------------------------------------------------------
    # Приватный хелпер
    # ------------------------------------------------------------------

    async def _get_by_field(self, field_name: str, value: str | UUID) -> Optional[AuthUser]:
        """
        Внутренний универсальный поиск.
        Не вызывайте напрямую из роутов — используйте публичные методы.
        """
        column = getattr(AuthUser, field_name)
        stmt = select(AuthUser).where(column == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()