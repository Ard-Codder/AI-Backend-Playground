# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt pyproject.toml ./

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем код приложения
COPY backend/ ./backend/
COPY ml_core/ ./ml_core/

# Устанавливаем приложение в режиме разработки
RUN pip install -e .

# Создаем пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
