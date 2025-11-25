# Actions — CI/CD Pipeline с GitHub Actions

Учебный проект, демонстрирующий настройку полного CI/CD pipeline для автоматической сборки Docker-образа и деплоя на сервер с использованием GitHub Actions.

## 📑 Оглавление

- [Демо](#-демо)
- [Описание](#-описание)
- [Технологии](#-технологии)
- [Структура проекта](#-структура-проекта)
- [Скриншоты](#-скриншоты)
- [API Эндпоинты](#-api-эндпоинты)
- [Локальный запуск](#-локальный-запуск)
- [CI/CD Pipeline](#️-cicd-pipeline)
- [Подготовка сервера](#-подготовка-сервера)
- [Переменные окружения](#-переменные-окружения)
- [Dockerfile](#-dockerfile-backend)
- [Документация](#-документация)

## 🚀 Демо

- **Backend API:** http://194.58.126.39:5001/
- **Frontend UI:** http://194.58.126.39:4173/

## 📋 Описание

REST API на Flask с веб-интерфейсом. При каждом push в ветку `main` автоматически:
1. Собирается Docker-образ
2. Публикуется в GitHub Container Registry (ghcr.io)
3. Деплоится на удалённый сервер через SSH

## 🛠 Технологии

| Технология | Назначение |
|------------|------------|
| **Python 3.12** | Язык программирования backend |
| **Flask 3.0** | Web-фреймворк для REST API |
| **Node.js 18** | Runtime для frontend |
| **Express** | Web-сервер для frontend |
| **Docker** | Контейнеризация приложения |
| **Docker Compose** | Оркестрация контейнеров |
| **GitHub Actions** | CI/CD pipeline |
| **GitHub Container Registry** | Хранение Docker-образов (ghcr.io) |
| **SSH** | Деплой на сервер через appleboy/ssh-action |

## 📁 Структура проекта

```
Actions/
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions workflow
├── docs/
│   ├── Требования.md            # Требования к проекту
│   └── Отчет_о_тестировании.md  # Отчёт о тестировании
├── frontend/
│   ├── public/
│   │   ├── index.html           # HTML страница
│   │   ├── app.js               # JavaScript логика
│   │   └── styles.css           # Стили
│   ├── Dockerfile               # Dockerfile для frontend
│   ├── package.json             # Зависимости Node.js
│   └── server.js                # Express сервер с proxy
├── screenshots/
│   ├── Скрин github actions.png # Скриншот GitHub Actions
│   └── Скрин HTTP-обработчика.png # Скриншот работы приложения
├── app.py                       # Flask backend
├── Dockerfile                   # Dockerfile для backend
├── docker-compose.yml           # Docker Compose конфигурация
├── requirements.txt             # Зависимости Python (Flask, flask-cors)
├── env.example                  # Пример файла с секретами
├── .dockerignore                # Исключения для Docker build
├── LICENSE                      # MIT лицензия
├── .gitignore                   # Исключения для Git
└── README.md                    # Этот файл
```

## 📸 Скриншоты

### GitHub Actions Workflow
![GitHub Actions](screenshots/Скрин%20github%20actions.png)

### Работа HTTP-обработчика
![HTTP Handler](screenshots/Скрин%20HTTP-обработчика.png)

## 🔌 API Эндпоинты

| Эндпоинт | Метод | Описание | Пример ответа |
|----------|-------|----------|---------------|
| `/` | GET | Главная страница со списком эндпоинтов | `{"message": "...", "endpoints": {...}}` |
| `/health` | GET | Проверка здоровья приложения | `{"status": "ok", "details": "..."}` |
| `/info` | GET | Метаданные о приложении | `{"app": "my-flask-app", "version": "1.0.0", "port": "5001"}` |
| `/env` | GET | Переменные окружения | `{"env": {"PORT": "5001", "HOSTNAME": "..."}}` |
| `/multiply/<a>/<b>` | GET | Умножение двух чисел | `{"operation": "multiply", "a": 3, "b": 4, "result": 12}` |
| `/divide/<a>/<b>` | GET | Деление двух чисел | `{"operation": "divide", "a": 10, "b": 2, "result": 5}` |

## 🚀 Локальный запуск

### Без Docker

```bash
# Клонировать репозиторий
git clone https://github.com/avkorolyov/Actions.git
cd Actions

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
python app.py

# Проверить
curl http://localhost:5001/health
```

### С Docker Compose (backend + frontend)

```bash
# Запустить полный стек
docker compose up --build

# Backend: http://localhost:5001
# Frontend: http://localhost:4173

# Остановить
docker compose down
```

### Только backend с Docker

```bash
# Собрать образ
docker build -t my-flask-app .

# Запустить контейнер
docker run -d -p 5001:5001 --name my-flask-app my-flask-app

# Проверить
curl http://localhost:5001/health

# Остановить
docker stop my-flask-app && docker rm my-flask-app
```

### Из GitHub Container Registry

```bash
# Загрузить образ
docker pull ghcr.io/avkorolyov/actions:latest

# Запустить контейнер
docker run -d -p 5001:5001 --name my-flask-app ghcr.io/avkorolyov/actions:latest
```

## ⚙️ CI/CD Pipeline

### Workflow: Build and Deploy

**Триггер:** Push в ветку `main`

**Job 1: Build and Push Docker Image**
- Checkout кода
- Настройка Docker Buildx
- Логин в GitHub Container Registry
- Сборка Docker-образа
- Push образа в ghcr.io с тегами:
  - `latest`
  - `main`
  - `main-<sha>`

**Job 2: Deploy to Server**
- Подключение к серверу через SSH (appleboy/ssh-action)
- Остановка старого контейнера
- Загрузка нового образа из ghcr.io
- Запуск нового контейнера
- Проверка статуса

### Настройка секретов

В настройках репозитория (Settings → Secrets and variables → Actions) необходимо добавить:

| Секрет | Описание |
|--------|----------|
| `SSH_HOST` | IP-адрес или домен сервера |
| `SSH_USER` | Имя пользователя для SSH (например, `deploy`) |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ (без passphrase) |
| `GHCR_TOKEN` | (опционально) PAT для pull приватных образов |

**Примечание:** `GITHUB_TOKEN` создаётся автоматически и используется для push образа в ghcr.io.

## 🖥 Подготовка сервера

### 1. Создание пользователя deploy

```bash
# Подключиться под root
ssh root@YOUR_SERVER_IP

# Создать пользователя
adduser deploy --disabled-password --gecos ""

# Добавить в группу docker
usermod -aG docker deploy

# Настроить SSH-ключ
mkdir -p /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
```

### 2. Добавление SSH-ключа

```bash
# На локальной машине — создать ключ без passphrase
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N ""

# Скопировать публичный ключ на сервер
cat ~/.ssh/deploy_key.pub | ssh root@YOUR_SERVER_IP "cat >> /home/deploy/.ssh/authorized_keys"

# Установить права на сервере
ssh root@YOUR_SERVER_IP "chmod 600 /home/deploy/.ssh/authorized_keys && chown -R deploy:deploy /home/deploy/.ssh"
```

### 3. Проверка подключения

```bash
ssh -i ~/.ssh/deploy_key deploy@YOUR_SERVER_IP
docker ps
```

### 4. Добавление ключа в GitHub

```bash
# Получить содержимое приватного ключа
cat ~/.ssh/deploy_key
```

Скопируйте вывод и добавьте в секрет `SSH_PRIVATE_KEY` на GitHub.

## 📝 Переменные окружения

### Backend

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `PORT` | Порт приложения | `5001` |

### Frontend

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `PORT` | Порт frontend | `4173` |
| `BACKEND_URL` | URL backend API | `http://backend:5001` |

## 🔧 Dockerfile (Backend)

```dockerfile
FROM python:3.12-slim

# Установка curl для healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

ENV PORT=5001

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

CMD ["python", "app.py"]
```

## 📚 Документация

- [Требования к проекту](docs/Требования.md)
- [Архитектура](docs/Архитектура.md)
- [Отчёт о тестировании](docs/Отчет_о_тестировании.md)

## 👤 Автор

Alexandr Korolyov

## 📄 Лицензия

MIT
