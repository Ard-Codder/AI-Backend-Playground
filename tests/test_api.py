"""
Интеграционные тесты для API
"""

import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.app.config import settings
from backend.app.db import Base, get_db
from backend.app.main import app

# Тестовая база данных
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    """Переопределение зависимости для тестов"""
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="session")
def event_loop():
    """Создание event loop для тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Настройка тестовой базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class TestHealthCheck:
    """Тесты проверки состояния API"""

    def test_root_endpoint(self):
        """Тест корневого эндпоинта"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == settings.VERSION

    def test_health_endpoint(self):
        """Тест эндпоинта здоровья"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "environment" in data


class TestAuthentication:
    """Тесты аутентификации"""

    def test_register_user(self):
        """Тест регистрации пользователя"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User",
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "id" in data
        assert "hashed_password" not in data  # Пароль не должен возвращаться

    def test_register_duplicate_user(self):
        """Тест регистрации дублирующегося пользователя"""
        user_data = {
            "email": "duplicate@example.com",
            "username": "duplicateuser",
            "password": "testpassword123",
        }

        # Первая регистрация
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 200

        # Попытка дублирования
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400

    def test_login_user(self):
        """Тест входа пользователя"""
        # Сначала регистрируем пользователя
        user_data = {
            "email": "login@example.com",
            "username": "loginuser",
            "password": "testpassword123",
        }

        register_response = client.post("/api/v1/auth/register", json=user_data)
        assert register_response.status_code == 200

        # Теперь входим
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"],
        }

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Тест входа с неверными данными"""
        login_data = {"username": "nonexistent", "password": "wrongpassword"}

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401


class TestTasks:
    """Тесты для работы с задачами"""

    def setup_method(self):
        """Подготовка для каждого теста"""
        # Регистрируем пользователя и получаем токен
        import time

        timestamp = int(time.time())
        user_data = {
            "email": f"taskuser{timestamp}@example.com",
            "username": f"taskuser{timestamp}",
            "password": "testpassword123",
        }

        register_response = client.post("/api/v1/auth/register", json=user_data)
        assert register_response.status_code == 200

        login_data = {
            "username": user_data["username"],
            "password": user_data["password"],
        }

        login_response = client.post("/api/v1/auth/login", data=login_data)
        assert login_response.status_code == 200

        token_data = login_response.json()
        self.token = token_data["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_create_task(self):
        """Тест создания задачи"""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium",
        }

        response = client.post("/api/v1/tasks/", json=task_data, headers=self.headers)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert "id" in data
        assert "created_at" in data

    def test_get_tasks(self):
        """Тест получения списка задач"""
        # Сначала создаем задачу
        task_data = {
            "title": "Test Task for List",
            "description": "Task for testing list endpoint",
        }

        create_response = client.post(
            "/api/v1/tasks/", json=task_data, headers=self.headers
        )
        assert create_response.status_code == 200

        # Получаем список задач
        response = client.get("/api/v1/tasks/", headers=self.headers)
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        response = client.get("/api/v1/tasks/")
        assert response.status_code == 403


class TestML:
    """Тесты для ML эндпоинтов"""

    def setup_method(self):
        """Подготовка для каждого теста"""
        # Регистрируем пользователя и получаем токен
        user_data = {
            "email": "mluser@example.com",
            "username": "mluser",
            "password": "testpassword123",
        }

        client.post("/api/v1/auth/register", json=user_data)
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"],
        }

        login_response = client.post("/api/v1/auth/login", data=login_data)
        token_data = login_response.json()
        self.token = token_data["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_ml_info(self):
        """Тест информации о ML алгоритмах"""
        response = client.get("/api/v1/ml/", headers=self.headers)
        assert response.status_code == 200

        data = response.json()
        assert "available_algorithms" in data
        assert "version" in data
        assert len(data["available_algorithms"]) >= 3
