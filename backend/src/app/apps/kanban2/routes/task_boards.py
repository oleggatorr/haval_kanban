from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from ..schemas.task_board import (
    TaskBoardCreate,
    TaskBoardUpdate,
    TaskBoardResponse,
    TaskBoardListResponse
)
from ..services.task_board_service import TaskBoardService

router = APIRouter()


def get_task_board_service(db: AsyncSession = Depends(get_db)) -> TaskBoardService:
    """Dependency для получения сервиса досок задач."""
    return TaskBoardService(db)


@router.get("/", response_model=TaskBoardListResponse)
async def get_boards(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Элементов на странице"),
    is_active: bool | None = Query(None, description="Фильтр по активности"),
    project_id: int | None = Query(None, description="Фильтр по проекту"),
    service: TaskBoardService = Depends(get_task_board_service)
):
    """Получить список досок задач с пагинацией."""
    
    boards, total = await service.get_boards(
        page=page,
        page_size=page_size,
        is_active=is_active,
        project_id=project_id
    )
    
    return TaskBoardListResponse(
        items=[TaskBoardResponse.model_validate(b) for b in boards],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{board_id}", response_model=TaskBoardResponse)
async def get_board(
    board_id: int,
    service: TaskBoardService = Depends(get_task_board_service)
):
    """Получить доску задач по ID."""
    
    board = await service.get_board_by_id(board_id)
    
    if not board:
        raise HTTPException(status_code=404, detail="Доска задач не найдена")
    
    return TaskBoardResponse.model_validate(board)


@router.get("/by-project/{project_id}", response_model=TaskBoardResponse)
async def get_board_by_project(
    project_id: int,
    service: TaskBoardService = Depends(get_task_board_service)
):
    """Получить доску задач по ID проекта."""
    
    board = await service.get_board_by_project_id(project_id)
    
    if not board:
        raise HTTPException(status_code=404, detail="Доска задач для данного проекта не найдена")
    
    return TaskBoardResponse.model_validate(board)


@router.post("/", response_model=TaskBoardResponse, status_code=201)
async def create_board(
    board_data: TaskBoardCreate,
    service: TaskBoardService = Depends(get_task_board_service)
):
    """Создать новую доску задач для проекта."""
    
    try:
        board = await service.create_board(board_data)
        return TaskBoardResponse.model_validate(board)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания доски: {str(e)}")


@router.patch("/{board_id}", response_model=TaskBoardResponse)
async def patch_board(
    board_id: int,
    board_data: TaskBoardUpdate,
    service: TaskBoardService = Depends(get_task_board_service)
):
    """Частично обновить доску задач."""
    
    board = await service.update_board(board_id, board_data)
    
    if not board:
        raise HTTPException(status_code=404, detail="Доска задач не найдена")
    
    return TaskBoardResponse.model_validate(board)


@router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    hard: bool = Query(False, description="Полное удаление (true) или мягкое (false)"),
    service: TaskBoardService = Depends(get_task_board_service)
):
    """Удалить доску задач."""
    
    if hard:
        success = await service.hard_delete_board(board_id)
    else:
        success = await service.delete_board(board_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Доска задач не найдена")
    
    return {"message": "Доска задач успешно удалена"}