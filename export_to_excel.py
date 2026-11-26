import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def export_orders():
    engine = create_async_engine(DATABASE_URL)

    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT id, user_id, name, phone, created_at FROM orders"))
        rows = result.fetchall()

        df = pd.DataFrame(rows, columns=["ID", "Telegram ID", "Имя", "Телефон", "Дата"])
        df.to_excel("orders_export.xlsx", index = False)
        print("Файл orders_export.xlsx успешно создан!")

if __name__ == "__main__":
    asyncio.run(export_orders())