import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config
# extended imports

logger = logging.getLogger(__name__)


async def register_all_commands(bot: Bot):
    await bot.set_my_commands([
        # extended commands
    ])


def register_all_middlewares(dp):
    "register all middlewares"
    # extended middlewares


def register_all_filters(dp):
    "register all filters"
    # extended filters


def register_all_handlers(dp):
    "register all handlers"
    # extended handlers


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="{parse_mode}")
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await register_all_commands(bot)
    

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")