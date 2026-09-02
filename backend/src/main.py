from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from .config.settings import settings

from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .middleware.LoggingMiddleware import LoggingMiddleware, setup_logging

# from src.app.home.routes import router as home_router

# from src.app.users.routes import router as user_router
# from src.app.users.routes_auth import router as auth_router

# from src.app.kanban._01_project.routes import router as project_router
# from src.app.kanban._02_tab.routes import router as tab_router
# from src.app.kanban._03_column.routes import router as column_router
# from src.app.kanban._04_task.routes import router as task_router
# from src.app.kanban._05_sub_task.routes import router as sub_task_router



from src.app.zup.zup_routes import register_zup_routers, zup_app

from src.app.user_auth.user_auth_routes import register_auth, base_users_app

from src.app.apps.kanban.init_routes import register_kanban_routes, kanban_app


import src.app._init_models



# Создание FastAPI приложения
app = FastAPI(
    title= f"ABOBA {settings.HOST}",
    description="Secure REST `API` for SAP HANA Database with CSRF protection",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)




# register_zup_routers(app)
app.mount("/zup", zup_app)

# register_kanban_routes(app)
app.mount("/kanban", kanban_app)


register_auth(app)
# app.mount("/user",base_users_app)

app.add_middleware(LoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "X-CSRF-Token"],  
)