"""
Роуты для работы с задачами
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.auth.security import get_current_active_user
from app.models.user import User
from app.models.task import TaskStatus

router = APIRouter()


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """Создание новой задачи"""
    task_service = TaskService(db)
    task = await task_service.create_task(task_data, current_user.id)
    return TaskResponse.model_validate(task)


@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[TaskStatus] = Query(None, description="Фильтр по статусу"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> List[TaskResponse]:
    """Получение списка задач текущего пользователя"""
    task_service = TaskService(db)
    tasks = await task_service.get_tasks(
        owner_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit
    )
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/stats")
async def get_task_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Получение статистики задач пользователя"""
    task_service = TaskService(db)
    stats = await task_service.get_user_tasks_count(current_user.id)
    return stats


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """Получение задачи по ID"""
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """Обновление задачи"""
    task_service = TaskService(db)
    task = await task_service.update_task(task_id, task_update, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Удаление задачи"""
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    
    return {"message": "Задача успешно удалена"}
