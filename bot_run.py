from aiogram import Dispatcher

from create_bot import dp
from tg_bot.database.start_gino import start_db_gino
from tg_bot.utils.notify_admins import on_startup_notify, off_stop_notify
from tg_bot.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher: Dispatcher):
    await start_db_gino(dp)
    await on_startup_notify(dp)
    await set_default_commands(dp)


async def on_shutdown(dispatcher: Dispatcher):
    await off_stop_notify(dp)


if __name__ == "__main__":
    import logging
    from aiogram.utils import executor

    # from tg_bot.middlewares import register_all_middlewares
    from tg_bot.filters import register_all_filters
    from tg_bot.handlers import register_all_handlers

    # register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    level = logging.INFO
    format = u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'

    # file_logger = logging.getLogger(__name__)
    # logging.basicConfig(
    #     level=level,
    #     filename=LOG_PATH,
    #     format=format
    # )

    console_logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=level,
        format=format
    )

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
