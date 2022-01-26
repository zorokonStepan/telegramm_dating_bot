from asyncio import sleep

from aiogram import types
from aiogram.utils.exceptions import BadRequest
from aiogram.utils.markdown import hbold

from config import time_sleep
from create_bot import bot

'''функции для оптимизации кода в хендлерах'''


async def sleep_del_msg_message(msg, message):
    await sleep(time_sleep)
    await msg.delete()
    await message.delete()


async def state_finish_sleep_bot_del_msg_message_delete(message, state, msg):
    await state.finish()
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await message.delete()


async def sleep_bot_delete_msg_message_delete(msg, message):
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await message.delete()


async def state_save_data_sleep_bot_delete_msg(state, callback_data, msg):
    async with state.proxy() as data:
        data["callback_data"] = callback_data
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


async def sleep_bot_del_msg(msg):
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


# ---------------------------------------------------------------------------------------------------------------------

# заголовок для просмотра карточек пользователей управляющими  
async def get_caption_for_managers(client):
    # вся информация о клиенте кроме {user.biography=}
    # иначе -> aiogram.utils.exceptions.BadRequest: Media_caption_too_long
    caption = f"{client.client_state=}, {client.user_id=}, @{client.username}, {client.name=}, {client.age=} ." \
              f"{client.gender=}, {client.latitude=}, {client.longitude=}" \
              f"{client.search_gender=}, {client.search_age=}, {client.time_banned=}, {client.search_latitude=}," \
              f"{client.search_longitude}, {client.search_radius=}"
    return caption


# заголовок для просмотра карточки управляющего админами и супер_админами
async def get_caption_manager(manager):
    caption = f"{manager.user_id=} username: @{manager.username}, {manager.manager_post=}."
    return caption


# заголовок для просмотра своей карточки
async def get_self_caption_users(user):
    caption = f"Фотографий не может быть меньше 1 шт и больше 10 шт\n" \
              f"Мое имя: {user.name}, мне: {user.age}, @{user.username}.\n{user.biography}"
    return caption


# заголовок для просмотра своей карточки и изменения своих фото
async def get_self_caption_for_change_photo_users(user):
    caption = f"Фотографий не может быть меньше 1 шт и больше 10 шт\n@{user.username}"
    return caption


# заголовок для просмотра карточки пользователя в роли клиента без взаимной симпатии
async def get_caption_users(user):
    caption = f"Мое имя: {user.name}, мне: {user.age}\n{user.biography}"
    return caption


# заголовок для просмотра карточки пользователя в роли клиента при взаимной симпатии
async def get_caption_mutual_users(user):
    caption = f'''Мое имя: {user.name}, мне: {user.age}, {hbold(f"связаться со мной: @{user.username}")},
     \n{user.biography}'''
    return caption


# шапка - приветствие для клавиатур
async def welcome_cap(msg):
    if msg.from_user.full_name:
        return f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}"
    return f"Добро пожаловать в Бот Знакомств"


async def welcome_block_call(call: types.CallbackQuery, kb, welcome):
    try:
        await call.message.edit_text(text=welcome, reply_markup=kb)
    except BadRequest:
        await call.message.delete()
        await call.message.answer(text=welcome, reply_markup=kb)


async def welcome_block_message(message: types.Message, kb, welcome):
    try:
        await message.edit_text(text=welcome, reply_markup=kb)
    except BadRequest:
        await message.delete()
        await message.answer(text=welcome, reply_markup=kb)
