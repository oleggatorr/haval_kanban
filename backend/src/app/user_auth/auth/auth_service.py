from uuid import UUID
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi import HTTPException, status

from ..users.service import UserService
from src.core.security.jwt import create_access_token, create_refresh_token, decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def authenticate_by_login(self, login: str, password: str) -> TokenPair:
        """
        Аутентификация по логину и паролю.
        Возвращает пару токенов при успехе или выбрасывает 401.
        """
        user = await self.user_service.get_user_by_login( login)

        # Единая ошибка для отсутствия пользователя и неверного пароля
        if not user or not pwd_context.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated",
            )

        return self._generate_token_pair(user.employee_id)

    async def refresh_tokens(self, refresh_token: str) -> TokenPair:
        """
        Обновление токенов по refresh_token.
        При валидном refresh_token выдается новая пара (access + refresh).
        """
        payload = decode_token(refresh_token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Проверяем тип токена
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is not a refresh token",
            )

        user_employee_id = payload.get("sub")
        if user_employee_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        # Проверяем, что пользователь всё ещё существует и активен
        user = await self.user_service.get_user_by_employee_id(user_employee_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists or is deactivated",
            )

        return self._generate_token_pair(user.employee_id)

    def _generate_token_pair(self, user_employee_id: UUID) -> TokenPair:
        """
        Генерация пары токенов для пользователя.
        Передаёт dict, как требует сигнатура jwt-модуля.
        """
        subject = str(user_employee_id)
        return TokenPair(
            access_token=create_access_token({"sub": subject, "type": "access"}),
            refresh_token=create_refresh_token({"sub": subject}),
        )