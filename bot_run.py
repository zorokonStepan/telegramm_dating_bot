from aiogram import Dispatcher

from create_bot import dp
from tg_bot.database.start_gino import start_db_gino
from tg_bot.utils.notify_admins import on_startup_notify, off_stop_notify
from tg_bot.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher: Dispatcher):
    # запуск БД
    await start_db_gino(dp)
    # команды при старте бота
    await on_startup_notify(dp)
    # команды которые бот будет предлагать
    await set_default_commands(dp)


async def on_shutdown(dispatcher: Dispatcher):
    # команды при остановке бота
    await off_stop_notify(dp)


if __name__ == "__main__":
    import logging
    from aiogram.utils import executor

    from tg_bot.filters import register_all_filters
    from tg_bot.handlers import register_all_handlers

    register_all_filters(dp)
    register_all_handlers(dp)

    # логгирование
    level = logging.INFO
    format = u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'

    # либо в файл
    # file_logger = logging.getLogger(__name__)
    # logging.basicConfig(
    #     level=level,
    #     filename=LOG_PATH,
    #     format=format
    # )

    # либо в консоль
    console_logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=level,
        format=format
    )

    # запуск бота
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
