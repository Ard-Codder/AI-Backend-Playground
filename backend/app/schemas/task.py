"""
Pydantic схемы для задач
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.app.models.task import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    """Базовая схема задачи"""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Схема для создания задачи"""

    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None


class TaskInDB(TaskBase):
    """Схема задачи в базе данных"""

    id: int
    owner_id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskResponse(TaskBase):
    """Схема ответа с данными задачи"""

    id: int
    owner_id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
