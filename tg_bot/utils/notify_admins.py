import logging

from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound

from create_bot import bot
from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers


async def on_startup_notify(dp: Dispatcher):
    try:
        admins = await select_post_managers("admin")
        super_admins = await select_post_managers("super_admin")
        all_admins = admins + super_admins

        telegram_message = '<b>Администрирование</b>\n{}'.format("Бот включен.")
        for admin in all_admins:
            try:
                await bot.send_message(admin.user_id, telegram_message)
            except ChatNotFound:  # для тестовых пользователей
                pass

    except Exception as err:
        logging.exception(err)


async def off_stop_notify(dp: Dispatcher):
    try:
        admins = await select_post_managers("admin")
        super_admins = await select_post_managers("super_admin")
        all_admins = admins + super_admins

        telegram_message = '<b>Администрирование</b>\n{}'.format("Бот выключен.")
        for admin in all_admins:
            try:
                await bot.send_message(admin.user_id, telegram_message)
            except ChatNotFound:  # для тестовых пользователей
                pass

    except Exception as err:
        logging.exception(err)
