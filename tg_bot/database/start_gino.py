from aiogram import Dispatcher

from config import SUPER_ADMIN_ID, SUPER_ADMIN_STATUS, SUPER_ADMIN_USERNAME
from create_bot import db
import config
from tg_bot.database.schemas.users_commands.manager_commands_users_db import add_manager
from tg_bot.testing.added_clients import added_test_client


async def start_db_gino(dp: Dispatcher):
    print("*****Установка связи с PostgreSQL*****")
    await db.set_bind(config.POSTGRES_URI)
    print("*****Готово*****")

    print("*****Удаляем все содержимое таблиц в базе данных*****")
    await db.gino.drop_all()
    print("*****Готово*****")

    print("*****Создаем все наши таблицы*****")
    await db.gino.create_all()
    print("*****Готово*****")

    print("*****Добавляем первого админа - SUPER_ADMIN - только он сможет удалять и добавлять админов*****")
    await add_manager(SUPER_ADMIN_ID, SUPER_ADMIN_USERNAME, SUPER_ADMIN_STATUS)
    print("*****Готово*****")

    # await added_test_client()
