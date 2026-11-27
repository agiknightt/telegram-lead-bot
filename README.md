# telegram-lead-bot

Асинхронный Telegram-бот для приёма заявок от клиентов. Заявки сохраняются в PostgreSQL, а администратор выгружает их в Excel одной командой. Проект полностью упакован в Docker.

![Демонстрация работы бота](<img width="523" height="988" alt="telegram_bot" src="https://github.com/user-attachments/assets/abe584b5-6bee-44f5-bc98-f9d3db3bab4a" />)

## Возможности

- Регистрация пользователей в базе данных.
- Пошаговый сбор заявки через FSM: имя → телефон.
- Сохранение заявок в PostgreSQL.
- Админ-команда `/export`: выгружает все заявки в Excel и отправляет файл в чат Telegram.
- Секреты (токен, параметры БД) хранятся в `.env`, а не в коде.
- Запуск одной командой через Docker Compose.

## Стек

- Python 3.11
- aiogram 3.x
- SQLAlchemy 2.0 + asyncpg
- PostgreSQL
- Pandas (экспорт в Excel)
- Docker, Docker Compose

## Структура проекта

```text
telegram-lead-bot/
├── main.py              # точка входа, обработчики команд и сообщений
├── models.py            # модели SQLAlchemy
├── states.py            # состояния FSM
├── export_to_excel.py   # выгрузка заявок в Excel
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                 # создаётся локально, в репозиторий не попадает
```

## Быстрый старт

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/agiknightt/telegram-lead-bot.git
   cd telegram-lead-bot
   ```

2. Создайте файл `.env` в корне проекта:

   ```env
   BOT_TOKEN=ваш_токен_от_BotFather
   DATABASE_URL=postgresql+asyncpg://user:password@db:5432/bot_db
   ADMIN_ID=ваш_telegram_id
   ```

3. Запустите проект:

   ```bash
   docker compose up --build -d
   ```

4. Откройте бота в Telegram и отправьте `/start`.

Остановить проект: `docker compose down`.

## Команды

| Команда   | Кто может | Что делает                                   |
|-----------|-----------|----------------------------------------------|
| `/start`  | все       | запускает сбор заявки (имя → телефон)        |
| `/export` | админ     | присылает файл Excel со всеми заявками       |

## Что планирую добавить

- [ ] Тесты на Pytest
- [ ] Логирование вместо `print`
- [ ] Валидация номера телефона
- [ ] Файл `.env.example`


