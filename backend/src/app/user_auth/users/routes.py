from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from .schemas import UserCreate, UserUpdate, UserResponse, UserFullResponse
from .service import UserService

router = APIRouter()


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


# ------------------------------------------------------------------
# Создание / Список
# ------------------------------------------------------------------

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Создание нового пользователя с проверкой сотрудника в ZUP."""
    # Проверка уникальности логина
    existing = await service.get_user_by_login(user_in.login)
    if existing:
        raise HTTPException(status_code=409, detail="Login already exists")

    try:
        return await service.create_user(user_in)
    except ValueError as e:
        # Ошибка валидации из сервиса (сотрудник не найден в ZUP)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[UserResponse])
async def list_users(service: UserService = Depends(get_user_service)):
    """Вывод всех профилей пользователей."""
    return await service.get_all_users()


# ------------------------------------------------------------------
# Поиск по конкретным полям (СТАТИЧЕСКИЕ пути — ДО динамического {user_id})
# ------------------------------------------------------------------

@router.get("/by-login/{login}", response_model=UserResponse)
async def get_user_by_login(login: str, service: UserService = Depends(get_user_service)):
    """Получение пользователя по логину."""
    user = await service.get_user_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, service: UserService = Depends(get_user_service)):
    """Получение пользователя по email."""
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/by-employee/{employee_id}", response_model=UserFullResponse)
async def get_user_by_employee(employee_id: str, service: UserService = Depends(get_user_service)):
    """
    Получение полной информации о пользователе по табельному номеру.
    Включает актуальные данные из кадровой системы (ZUP).
    """
    user = await service.get_user_by_employee_id(employee_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------------------------------------------------------
# Операции по ID пользователя
# ------------------------------------------------------------------


@router.patch("/by-employee/{employee_id}", response_model=UserResponse)
async def update_user(
    employee_id: str,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    """
    Обновление данных пользователя по табельному номеру.
    Поиск выполняется по employee_id вместо внутреннего UUID.
    """
    try:
        user = await service.update_user(employee_id, user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{employee_id}/full", response_model=UserFullResponse)
async def get_user_full_info(
    employee_id: str,
    service: UserService = Depends(get_user_service)

):
    """"""
    try:
        user = await service.get_full_info(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user