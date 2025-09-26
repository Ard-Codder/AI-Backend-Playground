"""
Роуты для работы с задачами
"""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from ..auth.security import get_current_active_user
from ..db import get_db
from ..models.task import TaskStatus
from ..models.user import User
from ..schemas.task import TaskCreate, TaskResponse, TaskUpdate
from ..services.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskResponse)  # type: ignore
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Создание новой задачи"""
    task_service = TaskService(db)
    task = await task_service.create_task(task_data, int(current_user.id))
    return TaskResponse.model_validate(task)  # type: ignore


@router.get("/", response_model=List[TaskResponse])  # type: ignore
async def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[TaskStatus] = Query(None, description="Фильтр по статусу"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    """Получение списка задач текущего пользователя"""
    task_service = TaskService(db)
    tasks = await task_service.get_tasks(
        owner_id=int(current_user.id), status=status, skip=skip, limit=limit
    )
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/stats")  # type: ignore
async def get_task_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Получение статистики задач пользователя"""
    task_service = TaskService(db)
    stats = await task_service.get_user_tasks_count(int(current_user.id))
    return stats


@router.get("/{task_id}", response_model=TaskResponse)  # type: ignore
async def read_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Получение задачи по ID"""
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, int(current_user.id))

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )

    return TaskResponse.model_validate(task)  # type: ignore


@router.put("/{task_id}", response_model=TaskResponse)  # type: ignore
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Обновление задачи"""
    task_service = TaskService(db)
    task = await task_service.update_task(task_id, task_update, int(current_user.id))

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )

    return TaskResponse.model_validate(task)  # type: ignore


@router.delete("/{task_id}")  # type: ignore
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Удаление задачи"""
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id, int(current_user.id))

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )

    return {"message": "Задача успешно удалена"}
