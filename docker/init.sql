-- Инициализация базы данных

-- Создание схемы если не существует
CREATE SCHEMA IF NOT EXISTS public;

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Установка временной зоны
SET timezone = 'UTC';
