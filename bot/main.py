from aiogram import Bot, Dispatcher
import asyncio
from aiogram.enums import ParseMode

from bot.db.utils import create_db
from bot.settings import Config
from bot.handlers import router as task_router
from bot.commands import Commands


async def bot_start(bot: Bot):
    """ Функция срабатывает при запуске бота """
    await Commands.set_commands(bot)
    await create_db()


async def main():
    bot = Bot(token=Config.TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    dp.startup.register(bot_start)
    dp.include_router(task_router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        await bot.session.close()
        await dp.stop_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
