# src\app\zup\zup_routes.py
from fastapi import FastAPI, APIRouter

from .departments.routes import router as departments_router
from .users.routes import router as users_router

def register_zup_routers(app: FastAPI) -> None:
    app.include_router(departments_router, prefix="/departments",   tags=["zup_departments"])
    app.include_router(users_router, prefix="/users",               tags=["zup_users"])
    

zup_app = FastAPI(title="Api for zup DB")
register_zup_routers(zup_app)