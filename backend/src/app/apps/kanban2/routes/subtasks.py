from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from ..schemas.subtask import (
    SubTaskCreate, SubTaskUpdate, SubTaskResponse, 
    SubTaskListResponse, SubTaskReorderRequest
)
from ..services.subtask_service import SubTaskService

router = APIRouter()


def get_svc(db: AsyncSession = Depends(get_db)) -> SubTaskService:
    return SubTaskService(db)


@router.get("/by-parent/{parent_task_id}", response_model=list[SubTaskResponse])
async def get_by_parent(
    parent_task_id: int,
    svc: SubTaskService = Depends(get_svc)
):
    """Получить все подзадачи конкретной задачи."""
    items = await svc.get_subtasks_by_parent(parent_task_id)
    return [SubTaskResponse.model_validate(i) for i in items]


@router.get("/{subtask_id}", response_model=SubTaskResponse)
async def get_one(
    subtask_id: int,
    svc: SubTaskService = Depends(get_svc)
):
    item = await svc.get_subtask_by_id(subtask_id)
    if not item:
        raise HTTPException(404, "Подзадача не найдена")
    return SubTaskResponse.model_validate(item)


@router.post("/", response_model=SubTaskResponse, status_code=201)
async def create(
    data: SubTaskCreate,
    svc: SubTaskService = Depends(get_svc)
):
    try:
        item = await svc.create_subtask(data)
        return SubTaskResponse.model_validate(item)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.patch("/{subtask_id}", response_model=SubTaskResponse)
async def patch(
    subtask_id: int,
    data: SubTaskUpdate,
    svc: SubTaskService = Depends(get_svc)
):
    item = await svc.update_subtask(subtask_id, data)
    if not item:
        raise HTTPException(404, "Подзадача не найдена")
    return SubTaskResponse.model_validate(item)


@router.post("/reorder")
async def reorder(
    data: SubTaskReorderRequest,
    parent_task_id: int = Query(..., description="ID родительской задачи"),
    svc: SubTaskService = Depends(get_svc)
):
    try:
        await svc.reorder_subtasks(parent_task_id, data.subtask_ids)
        return {"message": "Порядок обновлен"}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.delete("/{subtask_id}")
async def delete(
    subtask_id: int,
    hard: bool = Query(False),
    svc: SubTaskService = Depends(get_svc)
):
    if not await svc.delete_subtask(subtask_id, hard):
        raise HTTPException(404, "Подзадача не найдена")
    return {"message": "Удалено"}