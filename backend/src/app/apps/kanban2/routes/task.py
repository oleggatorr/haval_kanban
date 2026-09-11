from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.connection import get_db
from ..schemas.task import *
from ..services.task_service import TaskService

router = APIRouter()

def get_svc(db: AsyncSession = Depends(get_db)): return TaskService(db)

@router.get("/by-column/{column_id}", response_model=list[TaskResponse])
async def get_by_col(column_id: int, svc: TaskService = Depends(get_svc)):
    return [TaskResponse.model_validate(t) for t in await svc.get_tasks_by_column(column_id)]

@router.get("/{task_id}", response_model=TaskResponse)
async def get_one(task_id: int, svc: TaskService = Depends(get_svc)):
    t = await svc.get_task_by_id(task_id)
    if not t: raise HTTPException(404, "Not found")
    return TaskResponse.model_validate(t)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create(data: TaskCreate, svc: TaskService = Depends(get_svc)):
    try:
        return TaskResponse.model_validate(await svc.create_task(data))
    except Exception as e:
        raise HTTPException(400, str(e))

@router.patch("/{task_id}", response_model=TaskResponse)
async def patch(task_id: int, data: TaskUpdate, svc: TaskService = Depends(get_svc)):
    t = await svc.update_task(task_id, data)
    if not t: raise HTTPException(404, "Not found")
    return TaskResponse.model_validate(t)

@router.post("/reorder")
async def reorder(data: TaskReorderRequest, col_id: int = Query(...), svc: TaskService = Depends(get_svc)):
    try:
        await svc.reorder_tasks(col_id, data.task_ids)
        return {"msg": "OK"}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/{task_id}")
async def delete(task_id: int, hard: bool = Query(False), svc: TaskService = Depends(get_svc)):
    if not await svc.delete_task(task_id, hard):
        raise HTTPException(404, "Not found")
    return {"msg": "Deleted"}