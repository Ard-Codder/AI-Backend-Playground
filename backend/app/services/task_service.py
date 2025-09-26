"""
Сервис для работы с задачами
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Сервис для работы с задачами"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_data: TaskCreate, owner_id: int) -> Task:
        """Создание новой задачи"""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            due_date=task_data.due_date,
            owner_id=owner_id,
        )

        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_task(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """Получение задачи по ID"""
        query = select(Task).where(Task.id == task_id)

        if owner_id is not None:
            query = query.where(Task.owner_id == owner_id)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_tasks(
        self,
        owner_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """Получение списка задач с фильтрацией"""
        query = select(Task)

        conditions = []
        if owner_id is not None:
            conditions.append(Task.owner_id == owner_id)
        if status is not None:
            conditions.append(Task.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_task(
        self, task_id: int, task_data: TaskUpdate, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """Обновление задачи"""
        query = select(Task).where(Task.id == task_id)

        if owner_id is not None:
            query = query.where(Task.owner_id == owner_id)

        result = await self.db.execute(query)
        db_task = result.scalar_one_or_none()

        if not db_task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)

        # Обновление времени завершения при изменении статуса на завершено
        if "is_completed" in update_data and update_data["is_completed"]:
            update_data["completed_at"] = datetime.utcnow()
            update_data["status"] = TaskStatus.COMPLETED
        elif "status" in update_data and update_data["status"] == TaskStatus.COMPLETED:
            update_data["is_completed"] = True
            update_data["completed_at"] = datetime.utcnow()

        for field, value in update_data.items():
            setattr(db_task, field, value)

        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete_task(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """Удаление задачи"""
        query = select(Task).where(Task.id == task_id)

        if owner_id is not None:
            query = query.where(Task.owner_id == owner_id)

        result = await self.db.execute(query)
        db_task = result.scalar_one_or_none()

        if not db_task:
            return False

        await self.db.delete(db_task)
        await self.db.commit()
        return True

    async def get_user_tasks_count(self, owner_id: int) -> dict:
        """Получение статистики задач пользователя"""
        all_tasks = await self.get_tasks(owner_id=owner_id, limit=1000)

        stats = {
            "total": len(all_tasks),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "cancelled": 0,
        }

        for task in all_tasks:
            stats[task.status.value] += 1

        return stats
