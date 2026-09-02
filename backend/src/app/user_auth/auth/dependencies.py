from uuid import UUID

import logging
from fastapi import Header, HTTPException, status

from src.core.security.jwt import decode_token


from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from src.core.security.jwt import decode_token
from ..users.service import UserService
from src.core.database.connection import get_db

logger = logging.getLogger(__name__)

security = HTTPBearer()

async def get_current_user(
    credentials = Depends(security),
    db = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(401, "Invalid token")
    

    employee_id = payload.get("sub")
    
    userService = UserService(db)
    
    user = await userService.get_user_by_employee_id( employee_id)

    
    if not user:
        raise HTTPException(404, "User not found")
    
    return user


async def extract_employee_id_from_request(request: Request) -> dict:
    """
    Извлекает employee_id из JWT-токена.
    Не обращается к БД — работает только с payload токена.
    """
    try:
        auth_header = request.headers.get("Authorization")
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        else:
            token = request.cookies.get("session_token")

        if not token:
            return {"employee_id": None}

        payload = decode_token(token)
        if not payload:
            return {"employee_id": None}

        employee_id = payload.get("sub")
        return {"employee_id": str(employee_id) if employee_id else None}

    except Exception as e:
        logger.debug(f"Не удалось извлечь employee_id из токена: {e}")
        return {"employee_id": None}
