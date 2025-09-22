# 🤖 AI Backend Playground

**Современный backend с ML алгоритмами, реализованными с нуля**

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)

---

## 🎯 Описание проекта

AI Backend Playground — это демонстрационный проект, созданный для портфолио и показа навыков разработки современных backend-приложений с интеграцией машинного обучения. Проект включает:

- **REST API** на FastAPI с JWT аутентификацией
- **Async/await** архитектура с PostgreSQL
- **ML алгоритмы** реализованные с нуля (K-Means, Decision Tree, Random Forest)
- **Docker контейнеризация** и CI/CD pipeline
- **Comprehensive testing** с pytest

## 🏗️ Архитектура

```
ai-backend-playground/
├── backend/              # FastAPI приложение
│   ├── app/
│   │   ├── models/       # SQLAlchemy модели
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Бизнес-логика
│   │   ├── schemas/      # Pydantic схемы
│   │   ├── auth/         # JWT аутентификация
│   │   ├── db.py         # Конфигурация БД
│   │   └── main.py       # Главный файл приложения
├── ml_core/              # ML библиотека
│   ├── kmeans.py         # K-Means кластеризация
│   ├── decision_tree.py  # Дерево решений
│   ├── random_forest.py  # Случайный лес
│   └── tests/            # Тесты ML алгоритмов
├── docker/               # Docker конфигурация
├── tests/                # Тесты API
├── .github/workflows/    # CI/CD pipeline
└── docs/                 # Документация
```

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11+
- Docker и Docker Compose
- Git

### 1. Клонирование и настройка

```bash
git clone https://github.com/yourusername/ai-backend-playground.git
cd ai-backend-playground

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
pip install -e .
```

### 2. Конфигурация

```bash
# Копирование примера конфигурации
copy env.example .env

# Отредактируйте .env файл, особенно SECRET_KEY для продакшена
```

### 3. Запуск с Docker

```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### 4. Проверка API

- **API документация**: http://localhost:8000/docs
- **ReDoc документация**: http://localhost:8000/redoc
- **Adminer (управление БД)**: http://localhost:8080
- **Health check**: http://localhost:8000/health

## 🔧 Использование API

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword123",
    "full_name": "Test User"
  }'
```

### Вход в систему

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword123"
```

### Создание задачи

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Изучить FastAPI",
    "description": "Освоить создание API с FastAPI",
    "priority": "high"
  }'
```

## 🤖 ML Алгоритмы

### K-Means кластеризация

```python
from ml_core import KMeans
import numpy as np

# Создание данных
X = np.random.rand(100, 2)

# Кластеризация
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)

print(f"Инерция: {kmeans.inertia:.2f}")
```

### CLI интерфейс

```bash
# K-Means
python -m ml_core.kmeans --data data.csv --clusters 3 --output results.csv

# Decision Tree
python -m ml_core.decision_tree --data data.csv --target target_column --max-depth 5

# Random Forest
python -m ml_core.random_forest --data data.csv --target target_column --n-estimators 100
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Только unit тесты
pytest tests/test_kmeans.py

# Только API тесты
pytest tests/test_api.py

# С покрытием кода
pytest --cov=backend --cov=ml_core
```

### Линтеры и форматирование

```bash
# Форматирование кода
black backend/ ml_core/ tests/

# Проверка стиля
flake8 backend/ ml_core/ tests/

# Проверка типов
mypy backend/ ml_core/

# Сортировка импортов
isort backend/ ml_core/ tests/
```

## 🐳 Docker команды

```bash
# Сборка образа
docker-compose build

# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f backend

# Остановка всех сервисов
docker-compose down

# Пересборка с очисткой
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📊 API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход

### Пользователи
- `GET /api/v1/users/me` - Профиль пользователя
- `PUT /api/v1/users/me` - Обновление профиля
- `DELETE /api/v1/users/me` - Удаление аккаунта

### Задачи
- `POST /api/v1/tasks/` - Создание задачи
- `GET /api/v1/tasks/` - Список задач
- `GET /api/v1/tasks/{id}` - Получение задачи
- `PUT /api/v1/tasks/{id}` - Обновление задачи
- `DELETE /api/v1/tasks/{id}` - Удаление задачи
- `GET /api/v1/tasks/stats` - Статистика задач

### Machine Learning
- `GET /api/v1/ml/` - Информация о ML алгоритмах
- `POST /api/v1/ml/upload-data` - Загрузка данных для анализа

## 🔐 Безопасность

- JWT токены с настраиваемым временем жизни
- Хеширование паролей с bcrypt
- CORS настройки
- Валидация входных данных с Pydantic
- SQL инъекции защита через SQLAlchemy

## 📈 Мониторинг и логирование

- Health check endpoints
- Structured logging
- Database connection monitoring
- API response time tracking

## 🚧 Планы развития

### Этап 2 (Недели 3-4): DevOps
- [ ] CI/CD pipeline с GitHub Actions
- [ ] Автоматические тесты на PR
- [ ] Деплой на облачные платформы
- [ ] Monitoring и alerting

### Этап 3 (Недели 5-6): ML расширения
- [ ] Интеграция ML алгоритмов в API
- [ ] Сохранение и загрузка моделей
- [ ] Batch processing для больших данных
- [ ] Model versioning

### Этап 4 (Недели 7-8): Продвинутые возможности
- [ ] Веб-интерфейс (React/Vue)
- [ ] Real-time notifications (WebSockets)
- [ ] Caching с Redis
- [ ] API rate limiting

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменений (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

## 📝 Лицензия

Распространяется под лицензией MIT. См. `LICENSE` для подробностей.

## 👨‍💻 Автор

**Ваше Имя**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [yourprofile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

⭐ Если проект был полезен, поставьте звездочку!
AI Backend Playground is a learning and practical project to demonstrate skills in Backend Development, Machine Learning, and AI Engineering. The goal is to build a unified codebase that covers a wide technology stack — from a simple CRUD service to advanced AI/ML solutions deployed in production.
