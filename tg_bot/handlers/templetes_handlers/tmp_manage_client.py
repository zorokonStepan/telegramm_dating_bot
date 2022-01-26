from aiogram.utils.exceptions import ChatNotFound

from config import TIME_BANNED
from create_bot import bot
from tg_bot.database.schemas.users_commands.client_commands_users_db import banned_all_time_client, \
    banned_at_time_client, update_state_client

from tg_bot.database.schemas.users_commands.common_commands_users_db import delete_user


async def tmp_banned_user_time_1(call, client_id):
    # ЗАБАНИТЬ НА ВРЕМЯ
    await call.answer()
    await banned_at_time_client(user_id=client_id)
    try:
        await bot.send_message(chat_id=client_id, text=f"Вы забанены на {TIME_BANNED} часов")
    except ChatNotFound:
        pass


# ЗАБАНИТЬ НАВСЕГДА
async def tmp_banned_user_all_time_1(call, client_id):
    await call.answer()
    await banned_all_time_client(user_id=client_id)
    try:
        await bot.send_message(chat_id=client_id, text="Вы забанены навсегда")
    except ChatNotFound:
        pass


async def tmp_banned_user_2(call, client):
    if client.client_state == "banned_client":
        await call.answer(text="Пользователь уже забанен. Разбаньте его и забаньте снова.")
    elif client.client_state != "client" and client.client_state != "banned_client":
        await call.answer(text="Можно забанить только пользователя в состоянии client")


# если пользователь прошел модерацию
async def tmp_moderation_wait_client_true(wait_client_id):
    await update_state_client(user_id=wait_client_id, client_state="client")
    try:
        await bot.send_message(chat_id=wait_client_id, text="Ваша анкета прошла проверку. Можете пользоваться ботом")
    except ChatNotFound:
        pass


# если пользователь не прошел модерацию, то сообщаем об этом пользователю и удаляем его из БД
async def tmp_moderation_wait_client_false(wait_client_id):
    try:
        await bot.send_message(chat_id=wait_client_id, text="Ваша анкета не прошла проверку. Можете заполнить ее снова")
    except ChatNotFound:
        pass
    await delete_user(user_id=wait_client_id)
