# Makefile для AI Backend Playground

.PHONY: help install dev test lint format docker-build docker-up docker-down clean

# Переменные
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker-compose

help: ## Показать справку по командам
	@echo "AI Backend Playground - Команды разработки"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Установка зависимостей
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

dev: ## Установка зависимостей для разработки
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .[dev]

test: ## Запуск всех тестов
	pytest -v --tb=short

test-cov: ## Запуск тестов с покрытием кода
	pytest --cov=backend --cov=ml_core --cov-report=html --cov-report=term

test-unit: ## Запуск только unit тестов
	pytest tests/test_kmeans.py tests/test_decision_tree.py -v

test-api: ## Запуск только API тестов
	pytest tests/test_api.py -v

lint: ## Проверка кода линтерами
	flake8 backend/ ml_core/ tests/
	mypy backend/ ml_core/

format: ## Форматирование кода
	black backend/ ml_core/ tests/
	isort backend/ ml_core/ tests/

format-check: ## Проверка форматирования без изменений
	black --check backend/ ml_core/ tests/
	isort --check-only backend/ ml_core/ tests/

run-local: ## Запуск API локально
	cd backend && $(PYTHON) -m app.main

run-dev: ## Запуск API в режиме разработки
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Сборка Docker образа
	$(DOCKER_COMPOSE) build

docker-up: ## Запуск всех сервисов в Docker
	$(DOCKER_COMPOSE) up -d

docker-up-logs: ## Запуск с отображением логов
	$(DOCKER_COMPOSE) up

docker-down: ## Остановка всех Docker сервисов
	$(DOCKER_COMPOSE) down

docker-restart: ## Перезапуск Docker сервисов
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d

docker-logs: ## Просмотр логов
	$(DOCKER_COMPOSE) logs -f

docker-clean: ## Очистка Docker (удаление volumes)
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

ml-kmeans: ## Запуск K-Means CLI (требует --data)
	$(PYTHON) -m ml_core.kmeans $(ARGS)

ml-tree: ## Запуск Decision Tree CLI (требует --data --target)
	$(PYTHON) -m ml_core.decision_tree $(ARGS)

ml-forest: ## Запуск Random Forest CLI (требует --data --target)
	$(PYTHON) -m ml_core.random_forest $(ARGS)

db-init: ## Инициализация базы данных
	alembic upgrade head

db-migration: ## Создание новой миграции (требует NAME="migration_name")
	alembic revision --autogenerate -m "$(NAME)"

clean: ## Очистка временных файлов
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

setup-env: ## Создание .env файла из примера
	copy env.example .env

check-all: format-check lint test ## Полная проверка кода

ci: format-check lint test ## CI pipeline

# Примеры использования:
#
# make install          # Установка зависимостей
# make dev              # Установка для разработки
# make test             # Запуск всех тестов
# make lint             # Проверка кода
# make format           # Форматирование кода
# make docker-up        # Запуск в Docker
# make ml-kmeans ARGS="--data data.csv --clusters 3"
# make db-migration NAME="add_user_table"
