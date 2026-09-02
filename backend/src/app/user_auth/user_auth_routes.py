# src\app\zup\zup_routes.py
from fastapi import FastAPI, APIRouter

from .users.routes import router as users_auth_router
from .auth.auth_routes import router as auth_router

def register_auth(app: FastAPI) -> None:
    app.include_router(users_auth_router, prefix="/auth_users",   tags=["auth_users"])
    app.include_router(auth_router, prefix="/auth",               tags=["auth"])


base_users_app = FastAPI(title="Base users App")
register_auth(base_users_app)