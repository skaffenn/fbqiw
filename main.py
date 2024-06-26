import asyncio
from aiogram import Bot, Dispatcher
from data import config
from handlers import router

bot = Bot(token=config.bot_token)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
