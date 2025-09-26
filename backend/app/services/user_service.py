"""
Сервис для работы с пользователями
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.password import get_password_hash, verify_password
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        """Создание нового пользователя"""
        hashed_password = get_password_hash(user_data.password)

        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=user_data.is_active,
        )

        try:
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Пользователь с таким email или username уже существует")

    async def get_user(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return user if user is not None else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return user if user is not None else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по username"""
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        return user if user is not None else None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Получение списка пользователей"""
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновление данных пользователя"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()

        if db_user is None:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        # Хеширование нового пароля если он передан
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user if db_user is not None else None
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Данные пользователя уже используются")

    async def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        user = await self.get_by_username(username)

        if not user:
            return None

        if not verify_password(password, str(user.hashed_password)):
            return None

        return user
