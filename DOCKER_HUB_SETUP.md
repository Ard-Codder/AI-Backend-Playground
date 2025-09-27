# Docker Hub Setup

## Быстрая настройка для CI/CD

### 1. Создайте Access Token в Docker Hub
1. Войдите в [hub.docker.com](https://hub.docker.com)
2. Account Settings → Security → New Access Token
3. Создайте токен с правами **Read, Write, Delete**
4. **Сохраните токен!**

### 2. Добавьте секреты в GitHub
1. Ваш репозиторий → Settings → Secrets and variables → Actions
2. Добавьте:
   - `DOCKER_USERNAME` - ваш Docker Hub username
   - `DOCKER_PASSWORD` - созданный Access Token

### 3. Готово!
Теперь CI/CD будет автоматически собирать и публиковать образы в Docker Hub при push в main ветку.

## Проверка
После настройки секретов сделайте push в main ветку и проверьте Actions tab.

## ✅ Статус: Готово!
- Docker Hub токен создан
- GitHub Secrets настроены
- CI/CD pipeline готов к работе
