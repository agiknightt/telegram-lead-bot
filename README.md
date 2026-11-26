# telegram-lead-bot
Telegram-бот для сбора заявок (Lead Bot)

Асинхронный Telegram-бот для приема заявок от клиентов с сохранением данных в PostgreSQL и выгрузкой в Excel. Проект полностью упакован в Docker.

## 🚀 Функционал
* Регистрация пользователей в базе данных.
* Пошаговый сбор заявок (FSM): имя -> телефон.
* Сохранение заявок в PostgreSQL.
* **Админ-панель:** команда `/export` выгружает все заявки в Excel и отправляет файл прямо в Telegram.
* Защита секретов (токены вынесены в `.env`).
* Полная контейнеризация (Docker Compose).

## 🛠 Стек технологий
* **Python 3.11**
* **aiogram 3.x** (асинхронный фреймворк для Telegram)
* **SQLAlchemy 2.0** + **asyncpg** (асинхронная работа с БД)
* **PostgreSQL** (база данных)
* **Pandas** (экспорт в Excel)
* **Docker** и **Docker Compose**

## ⚙️ Как запустить локально
1. Клонируйте репозиторий.
2. Создайте файл `.env` и добавьте:
   ```env
   BOT_TOKEN=ваш_токен
   DATABASE_URL=postgresql+asyncpg://user:password@db:5432/bot_db
   ADMIN_ID=ваш_telegram_id
```

3. Запустите проект одной командой:
   ```bash
   docker compose up --build -d
   ```

📸 Демонстрация работы
<img width="523" height="988" alt="telegram_bot" src="https://github.com/user-attachments/assets/abe584b5-6bee-44f5-bc98-f9d3db3bab4a" />
