# src\app\apps\kanban\user_profille\profille\profille_services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from typing import List, Dict, Any

from .profille_models import UserProfile
from .profille_schemas import UserProfileCreate, UserProfileUpdate, UserFullInfoResponse, UserProfileResponse, UserResponse
# Импортируем внешний сервис авторизации
from .....user_auth.users.service import UserService

from.permissions_servises import PermissionService


class UserProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session) 

    async def _verify_user_exists(self, employee_id: str) -> None:
        """Проверяет существование пользователя в auth_users через внешний сервис."""
        user = await self.user_service.get_user_by_employee_id(employee_id=employee_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с employee_id '{employee_id}' не найден в системе авторизации"
            )

    async def create_profile(self, data: UserProfileCreate) -> UserProfile:
        # 1. Проверяем, что пользователь существует в auth
        await self._verify_user_exists(data.employee_id)
        
        # 2. Проверяем, не создан ли уже профиль
        existing = await self.session.execute(
            select(UserProfile).where(UserProfile.employee_id == data.employee_id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Профиль для данного сотрудника уже существует"
            )

        profile = UserProfile(**data.model_dump())
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def get_profile(self, employee_id: str) -> UserProfile:
        result = await self.session.execute(
            select(UserProfile).where(UserProfile.employee_id == employee_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Профиль не найден")
        return profile
    
    async def get_full_user_info(self, employee_id: str) -> UserFullInfoResponse:
        """
        Получение полной информации о пользователе.
        Объединяет: профиль, данные auth и кадровую систему ZUP.
        """
        # 1. Профиль (обязателен)
        profile = await self.get_profile(employee_id)

        # 2. Данные auth + ZUP одним вызовом
        user_full = await self.user_service.get_full_info(employee_id)
        if not user_full:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден в системе авторизации"
            )

        # 3. Собираем итоговый ответ
        return UserFullInfoResponse(
            profile=UserProfileResponse.model_validate(profile),
            auth=UserResponse(**user_full.model_dump(exclude={"zup_info", "warning"})),
            zup_info=user_full.zup_info,
            warning=user_full.warning,
        )

    async def update_profile(self, employee_id: str, data: UserProfileUpdate) -> UserProfile:
        profile = await self.get_profile(employee_id)
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
            
        await self.session.commit()
    
    # ✅ 2. Обновляем объект из БД (получаем updated_at и другие поля)
        await self.session.refresh(profile)
        return profile

    async def delete_profile(self, employee_id: str) -> None:
        profile = await self.get_profile(employee_id)
        await self.session.delete(profile)
        await self.session.commit()
    

    async def grant_project_access(
        self, 
        employee_id: str, 
        project_id: int, 
        role: str = "viewer", 
        permissions: List[str] = None
    ) -> UserProfile:
        """
        Выдает доступ пользователю к проекту.
        """
        profile = await self.get_profile(employee_id)
        
        # Текущие права из БД
        current_perms = profile.permissions or {}
        
        # Обновляем структуру через PermissionService
        updated_perms = PermissionService.add_project_access(
            permissions=current_perms,
            project_id=project_id,
            role=role,
            perms=permissions
        )
        
        # Сохраняем обновленный JSON
        profile.permissions = updated_perms
        await self.session.commit()
        await self.session.refresh(profile)
        
        return profile

    async def revoke_project_access(
        self, 
        employee_id: str, 
        project_id: int
    ) -> UserProfile:
        """
        Отзывает доступ пользователя к проекту.
        """
        profile = await self.get_profile(employee_id)
        
        current_perms = profile.permissions or {}
        
        updated_perms = PermissionService.remove_project_access(
            permissions=current_perms,
            project_id=project_id
        )
        
        profile.permissions = updated_perms
        await self.session.commit()
        await self.session.refresh(profile)
        
        return profile

    async def set_system_role(
        self, 
        employee_id: str, 
        new_role: str
    ) -> UserProfile:
        """
        Изменяет системную роль пользователя (admin, manager, user).
        """
        profile = await self.get_profile(employee_id)
        
        current_perms = profile.permissions or {}
        
        # Обновляем роль в структуре system
        if "system" not in current_perms:
            current_perms["system"] = {}
            
        current_perms["system"]["role"] = new_role
        
        profile.permissions = current_perms
        await self.session.commit()
        await self.session.refresh(profile)
        
        return profile