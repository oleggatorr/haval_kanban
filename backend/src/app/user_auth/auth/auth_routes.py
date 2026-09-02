from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.app.user_auth.users.service import UserService
from src.app.user_auth.users.schemas import UserResponse
from .auth_schemas import LoginRequest, RefreshTokenRequest, TokenResponse
from src.app.user_auth.auth.auth_service import AuthService
from src.core.security.jwt import decode_token  # Для эндпоинта /me

from .dependencies import get_current_user

router = APIRouter()


def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    user_service = UserService(session)
    return AuthService(user_service)


async def _extract_user_from_token(
    authorization: str = Depends(lambda: None),  # Замените на реальную зависимость
) -> dict:
    """
    Вспомогательная зависимость для извлечения user_id из access_token.
    В продакшене вынесите это в отдельную зависимость get_current_user.
    """
    from fastapi import Header, HTTPException
    
    # Если используется Header напрямую:
    # async def _extract_user_from_token(authorization: str = Header(...)):
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    
    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    
    return {"user_id": payload["sub"]}


@router.post("/login", response_model=TokenResponse, summary="Аутентификация по логину")
async def login(
    credentials: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Обменивает логин и пароль на пару JWT-токенов.
    Возвращает 401 при неверных учетных данных.
    """
    return await service.authenticate_by_login(
        login=credentials.login,
        password=credentials.password,
    )


@router.post("/refresh", response_model=TokenResponse, summary="Обновление токенов")
async def refresh_tokens(
    body: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Принимает refresh_token и возвращает новую пару access + refresh токенов.
    Старый refresh_token становится недействительным (ротация).
    """
    return await service.refresh_tokens(body.refresh_token)


@router.get("/me", response_model=UserResponse, summary="Текущий пользователь")
async def get_me(
    service: AuthService = Depends(get_auth_service),
    # Предполагается, что у вас есть зависимость get_current_user_dependency,
    # которая извлекает токен из заголовка Authorization и декодирует его.
    # Ниже показана inline-реализация для самодостаточности:
    data: dict = Depends(get_current_user),
):
    """
    Возвращает профиль текущего аутентифицированного пользователя.
    Требует валидный access_token в заголовке Authorization: Bearer <token>
    """
    # user = await service.user_service.get_user_by_field("id", token_data["user_id"])
    # if not user or not user.is_active:
    #     from fastapi import HTTPException
    #     raise HTTPException(status_code=401, detail="User not found or deactivated")
    return data


