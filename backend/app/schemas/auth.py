"""
Pydantic схемы для аутентификации
"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Схема токена доступа"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Схема данных токена"""

    username: Optional[str] = None
    user_id: Optional[int] = None


class UserLogin(BaseModel):
    """Схема для входа пользователя"""

    username: str
    password: str
