import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from bot.handlers.start import router as start_router
from bot.handlers.tasks import router as tasks_router
from bot.handlers.chat import router as chat_router

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(tasks_router)
dp.include_router(chat_router)

async def main():
    print("oLLo запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())