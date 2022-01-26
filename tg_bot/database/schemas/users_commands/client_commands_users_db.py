from datetime import datetime

from asyncpg import UniqueViolationError
from sqlalchemy import or_

from tg_bot.database.schemas.users.users_db import UserDB

"""
команды с БД только для клиентов
"""


# добавить запись с новым клиентом
# age не может быть None т.к. сортировка списков по возрасту
async def add_client(user_id: int, username: str, client_state: str, age=0):
    try:
        client = UserDB(user_id=user_id, username=username, client_state=client_state, age=age,
                        photo=[], who_liked_me=[], users_i_liked=[], mutual_liking=[])
        await client.create()

    except UniqueViolationError:
        pass


# получение списка клиентов в одном состоянии
async def select_state_clients(client_state: str):
    clients = await UserDB.query.where(UserDB.client_state == client_state).gino.all()
    return clients


# получение списка клиентов трех состояний
async def select_states_clients(client_state_1: str, client_state_2: str, client_state_3: str):
    clients = await UserDB.query.where(or_(
        UserDB.client_state == client_state_1,
        UserDB.client_state == client_state_2,
        UserDB.client_state == client_state_3)
    ).gino.all()
    return clients


# изменение состояние клиента
async def update_state_client(user_id: int, client_state: str):
    client = await UserDB.get(user_id)
    await client.update(client_state=client_state).apply()


# забанить на время
async def banned_at_time_client(user_id: int):
    user = await UserDB.get(user_id)
    await user.update(time_banned=datetime.now()).apply()
    await user.update(client_state="banned_client").apply()


# забанить навсегда
async def banned_all_time_client(user_id: int):
    user = await UserDB.get(user_id)
    await user.update(time_banned=None).apply()
    await user.update(client_state="banned_client").apply()


# разбанить клиента
async def unbanned_client(user_id: int):
    user = await UserDB.get(user_id)
    await user.update(time_banned=None).apply()
    await user.update(client_state="client").apply()
