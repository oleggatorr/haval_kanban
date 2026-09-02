from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from .....user_auth.users.service import UserService
from .profille_schemas import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserFullInfoResponse,
)
from .profille_services import UserProfileService

router = APIRouter()


# ✅ Фабрика для UserService — указывает FastAPI, как его создавать
async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


# ✅ Теперь обе зависимости разрешаются корректно
async def get_profile_service(
    session: AsyncSession = Depends(get_db),
    # user_service: UserService = Depends(get_user_service),
) -> UserProfileService:
    return UserProfileService(session)


@router.post("", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    payload: UserProfileCreate,
    service: UserProfileService = Depends(get_profile_service),
):
    return await service.create_profile(payload)


@router.get("/{employee_id}/full", response_model=UserFullInfoResponse)
async def get_user_full_info(
    employee_id: str,
    service: UserProfileService = Depends(get_profile_service),
):
    """Полная информация: профиль + auth + ZUP."""
    return await service.get_full_user_info(employee_id)


@router.get("/{employee_id}", response_model=UserProfileResponse)
async def get_user_profile(
    employee_id: str,
    service: UserProfileService = Depends(get_profile_service),
):
    return await service.get_profile(employee_id)


@router.patch("/{employee_id}", response_model=UserProfileResponse)
async def update_user_profile(
    employee_id: str,
    payload: UserProfileUpdate,
    service: UserProfileService = Depends(get_profile_service),
):
    return await service.update_profile(employee_id, payload)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
    employee_id: str,
    service: UserProfileService = Depends(get_profile_service),
):
    await service.delete_profile(employee_id)