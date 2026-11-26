import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from models import Base, User
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states import OrderForm
from models import Order
import time
import pandas as pd
from aiogram.types import FSInputFile

load_dotenv()  # Загружаем переменные окружения из .env
BOT_BOTKEN = os.getenv("BOT_TOKEN")  # Получаем токен бота из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")  # Получаем URL базы данных из переменных окружения
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

bot = Bot(token=BOT_BOTKEN)
dp = Dispatcher()

start_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Оставить заявку")]],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            new_user = User(telegram_id=user_id, username=message.from_user.username)
            session.add(new_user)
            await session.commit()
            await message.answer(f"Привет, {user_name}! Я бот для портфолио. Готов к работе\n\n")
        else:
            await message.answer(f"С возвращением, {user_name}! Рад видеть тебя снова.\n\n")
        await message.answer("Выберите действие:", reply_markup=start_kb)

@dp.message(F.text == "Оставить заявку")
async def process_order_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer("Как вас зовут?", reply_markup=ReplyKeyboardRemove())

@dp.message(OrderForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.phone)
    await message.answer("Отлично! Теперь введите ваш номер телефона:")

@dp.message(OrderForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    phone = message.text

    async with async_session() as session:
        new_order = Order(user_id = message.from_user.id, name = name, phone = phone)
        session.add(new_order)
        await session.commit()

    await state.clear()

    await message.answer(
        f"Спасибо {name}! Ваша заявка принята. Мы свяжемся с вами!",
        reply_markup=start_kb
    )

@dp.message(Command("export"))
async def cmd_export(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для этой команды")
        return

    async with async_session() as session:
        stmt = select(Order).order_by(Order.id)
        result = await session.execute(stmt)
        orders = result.scalars().all()

        if not orders:
            await message.answer("Заявок пока нет.")
            return

        data = []
        for order in orders:
            data.append({
                "ID": order.id,
                "Telegram_ID": order.user_id,
                "Имя": order.name,
                "Телефон": order.phone,
                "Дата": order.created_at.strftime("%Y-%m-%d %H:%M")
            })
        df = pd.DataFrame(data)
        filename = f"orders_export_{int(time.time())}.xlsx"
        df.to_excel(filename, index = False)

        file_to_send = FSInputFile(filename)
        await message.answer_document(file_to_send, caption = "Актуальный список заявок")

async def main():
    print("Подключение к базе данных и создание таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")