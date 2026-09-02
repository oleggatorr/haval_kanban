# src\app\zup\zup_routes.py
from fastapi import FastAPI, APIRouter

from .directories._01_project.routes import router  as project_router
from .directories._02_tab.routes import router  as tab_router
from .directories._03_column.routes import router as column_router
from .directories._04_task.routes import router as task_router
from .directories._05_sub_task .routes import router as sub_task_router

from .user_profille.profille.profille_routes import router as profille_router
from .user_profille.auth.auth_routes import router as auth_router



def register_kanban_routes(app: FastAPI) -> None:
    ''''''
    app.include_router(auth_router, prefix="/auth",   tags=["auth_router"])
    app.include_router(profille_router, prefix="/profille",   tags=["profille_router"])

    
    app.include_router(project_router, prefix="/project",   tags=["project_router"])
    app.include_router(tab_router, prefix="/tab",   tags=["tab_router"])
    app.include_router(column_router, prefix="/column", tags= ["column_router"])
    app.include_router(task_router, prefix="/task", tags= ["task_router"])
    app.include_router(sub_task_router, prefix="/sub_task", tags= ["sub_task_router"])

kanban_app = FastAPI(title="Base users App")
register_kanban_routes(kanban_app)