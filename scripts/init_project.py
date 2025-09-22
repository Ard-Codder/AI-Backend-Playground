#!/usr/bin/env python3
"""
Скрипт инициализации проекта AI Backend Playground
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Выполнение команды с проверкой результата"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} - успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка: {e.stderr}")
        return False


def check_requirements():
    """Проверка системных требований"""
    print("🔍 Проверка системных требований...")
    
    # Проверка Python
    python_version = sys.version_info
    if python_version < (3, 11):
        print(f"❌ Требуется Python 3.11+, установлен {python_version.major}.{python_version.minor}")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Проверка Docker
    if not shutil.which("docker"):
        print("❌ Docker не найден. Установите Docker Desktop")
        return False
    print("✅ Docker найден")
    
    # Проверка Docker Compose
    if not shutil.which("docker-compose"):
        print("❌ Docker Compose не найден")
        return False
    print("✅ Docker Compose найден")
    
    return True


def setup_environment():
    """Настройка окружения"""
    print("\n🔧 Настройка окружения...")
    
    # Создание .env файла
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("✅ Создан .env файл из примера")
        print("⚠️  Обязательно измените SECRET_KEY в .env файле!")
    elif env_file.exists():
        print("ℹ️  .env файл уже существует")
    else:
        print("❌ env.example не найден")
        return False
    
    return True


def install_dependencies():
    """Установка зависимостей"""
    print("\n📦 Установка зависимостей...")
    
    commands = [
        ("python -m pip install --upgrade pip", "Обновление pip"),
        ("pip install -r requirements.txt", "Установка зависимостей"),
        ("pip install -e .", "Установка проекта в режиме разработки")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def setup_database():
    """Настройка базы данных"""
    print("\n🗄️  Настройка базы данных...")
    
    # Запуск PostgreSQL в Docker
    if not run_command("docker-compose up -d db", "Запуск PostgreSQL"):
        return False
    
    # Ожидание готовности БД
    print("⏳ Ожидание готовности базы данных...")
    import time
    time.sleep(10)
    
    return True


def run_tests():
    """Запуск тестов"""
    print("\n🧪 Запуск тестов...")
    
    if not run_command("pytest tests/ -v", "Выполнение тестов"):
        print("⚠️  Некоторые тесты могли не пройти - это нормально на начальном этапе")
    
    return True


def main():
    """Главная функция инициализации"""
    print("🚀 Инициализация AI Backend Playground")
    print("=" * 50)
    
    # Проверка требований
    if not check_requirements():
        print("\n❌ Системные требования не выполнены")
        sys.exit(1)
    
    # Настройка окружения
    if not setup_environment():
        print("\n❌ Ошибка настройки окружения")
        sys.exit(1)
    
    # Установка зависимостей
    if not install_dependencies():
        print("\n❌ Ошибка установки зависимостей")
        sys.exit(1)
    
    # Настройка базы данных
    if not setup_database():
        print("\n❌ Ошибка настройки базы данных")
        sys.exit(1)
    
    # Запуск тестов
    run_tests()
    
    print("\n🎉 Инициализация завершена!")
    print("\n📖 Следующие шаги:")
    print("1. Проверьте настройки в .env файле")
    print("2. Запустите API: make run-dev")
    print("3. Откройте документацию: http://localhost:8000/docs")
    print("4. Попробуйте ML алгоритмы: make ml-kmeans ARGS='--data data/sample_data.csv --clusters 3'")
    
    print("\n🔗 Полезные команды:")
    print("• make help           - Список всех команд")
    print("• make docker-up      - Запуск в Docker")
    print("• make test           - Запуск тестов")
    print("• make format         - Форматирование кода")


if __name__ == "__main__":
    main()
