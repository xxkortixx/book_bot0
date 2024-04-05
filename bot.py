import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
import handlers.questions as questions
from config import bot_token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)

dp = Dispatcher()

dp.include_router(questions.router)

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())