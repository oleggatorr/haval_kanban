# src\app\zup\zup_routes.py
from fastapi import FastAPI, APIRouter

from .project import router as project_router
from .task_boards import router as task_boards_router
from .task_columns import router as task_columns_router
from .task import router as task_router
from .subtasks import router as subtasks_router

def register_kanban2_routes(app: FastAPI) -> None:
    """"""
    app.include_router(project_router, prefix="/project",   tags=["project"])
    app.include_router(task_boards_router, prefix="/task_boards",   tags=["task_boards"])
    app.include_router(task_columns_router, prefix="/task_columns",   tags=["task_columns"])
    app.include_router(task_router, prefix="/task",   tags=["task"])
    app.include_router(subtasks_router, prefix="/subtasks",   tags=["subtasks"])



kanban2_app = FastAPI(title="Base users App")
register_kanban2_routes(kanban2_app)