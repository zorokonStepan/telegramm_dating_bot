from asyncio import sleep
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from config import time_sleep
from create_bot import bot
from tg_bot.database.schemas.users_commands import common_commands_users_db as commands
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user
from tg_bot.filters import IsSuperAdmin, IsAdmin
from tg_bot.keyboards.all_users.inline.all_users import get_gender_kb, get_search_gender_kb
from tg_bot.keyboards.callback_datas.cb_datas import gender_callback, change_user_card_callback
from tg_bot.keyboards.manager.inline.change_settings_client import get_change_settings_client_kb, \
    get_change_client_photo_kb
from tg_bot.misc.for_handlers import state_finish_sleep_bot_del_msg_message_delete, \
    sleep_bot_delete_msg_message_delete, state_save_data_sleep_bot_delete_msg
from tg_bot.misc.user_status import status_user
from tg_bot.states.state_change import AdminChangeClient


async def start_admin_change_settings_client(msg: Union[types.CallbackQuery, types.Message], callback_data: dict):
    user_status = await status_user(msg)
    category = callback_data.get("category")
    page = int(callback_data.get("page"))
    photo_page = int(callback_data.get("photo_page"))
    client_id = int(callback_data.get("user_id"))

    kb = get_change_settings_client_kb(user_status=user_status, category=category, page=page,
                                       photo_page=photo_page, user_id=client_id)

    if type(msg) == types.CallbackQuery:
        try:
            await msg.message.edit_text(text="Меню для изменения настроек пользователя", reply_markup=kb)
        except BadRequest:
            await msg.message.delete()
            await msg.message.answer(text="Меню для изменения настроек пользователя", reply_markup=kb)
    else:
        try:
            await msg.edit_text(text="Меню для изменения настроек пользователя", reply_markup=kb)
        except BadRequest:
            await msg.delete()
            await msg.answer(text="Меню для изменения настроек пользователя", reply_markup=kb)


async def admin_change_name_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите новое имя пользователя")
    await AdminChangeClient.Name.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_name_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_name(user_id=client_id, name=message.text)
        msg = await message.answer(f"У пользователя установлено новое имя: {message.text}")

        await start_admin_change_settings_client(message, callback_data)
        await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)


async def admin_change_age_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите возраст")
    await AdminChangeClient.Age.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_age_client(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            callback_data = data["callback_data"]
            client_id = int(callback_data.get("user_id"))
            await commands.update_user_age(user_id=client_id, age=int(message.text))
            msg = await message.answer(f"У пользователя установлен новый возраст: {message.text}")

            await start_admin_change_settings_client(message, callback_data)
            await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)

    else:
        msg = await message.answer("Введите возраст одним числом")

        await sleep_bot_delete_msg_message_delete(msg, message)


async def admin_change_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    kb = get_gender_kb(params=["base"])
    await call.message.delete()
    await call.message.answer("Выберите пол пользователя", reply_markup=kb)
    await AdminChangeClient.Gender.set()
    async with state.proxy() as data:
        data["callback_data"] = callback_data


async def load_admin_change_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_gender(user_id=client_id, gender=gender)
        await start_admin_change_settings_client(call, callback_data)
        await state.finish()


async def admin_change_biography_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Напишите биографию пользователя")
    await AdminChangeClient.Biography.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_biography_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_biography(user_id=client_id, biography=message.text)
        msg = await message.answer(f"У пользователя новая биография: {message.text}")

        await start_admin_change_settings_client(message, callback_data)
        await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)


async def admin_see_first_photo_client(call: types.CallbackQuery, callback_data: dict):
    client_id = int(callback_data.get("user_id"))
    category = callback_data.get("category")
    client = await commands.select_user(client_id)
    client_photo = client.photo

    user_status = await status_user(call)
    kb = get_change_client_photo_kb(user_status=user_status, category=category, page=1, photo_page=1,
                                    user_id=client_id, user_photo=client_photo)
    # информация о клиенте кроме {client.time_banned=}
    caption = f"{client.user_id=}, @{client.username}, {client.name=}, {client.age=} ." \
              f"{client.client_state=}, {client.gender=}, {client.latitude=}, {client.longitude=}" \
              f"{client.search_gender=}, {client.search_age=}, {client.search_latitude=}, {client.search_longitude}," \
              f"{client.search_radius=}\n{client.biography=}"

    await call.message.delete()
    await call.message.answer_photo(photo=client.photo[0], caption=caption, reply_markup=kb)


async def admin_see_photos_client(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    client_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    client = await commands.select_user(client_id)

    # информация о клиенте кроме {client.time_banned=}
    caption = f"{client.client_state=}\n{client.user_id=}, @{client.username}, {client.name=}, {client.age=} ." \
              f"{client.gender=}, {client.latitude=}, {client.longitude=}" \
              f"{client.search_gender=}, {client.search_age=}, {client.search_latitude=}, {client.search_longitude}," \
              f"{client.search_radius=}\n{client.biography=}"

    user_status = await status_user(call)

    kb = get_change_client_photo_kb(user_status=user_status, user_id=client_id, user_photo=client.photo, page=page,
                                    photo_page=photo_page, category=category)

    photo = InputMedia(type="photo", media=client.photo[photo_page - 1], caption=caption)

    await call.message.edit_media(media=photo, reply_markup=kb)


async def admin_change_photo_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    client_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    value = callback_data.get("value")
    client = await select_user(client_id)

    if value == "delete_photo":

        if len(client.photo) > 1:
            await call.answer()
            await commands.delete_user_photo(user_id=client_id, index_delete_photo=photo_page - 1)
            cb_data = callback_data
            # чтобы не выходить за index out of range
            if photo_page == 1:
                cb_data["photo_page"] = photo_page
            else:
                cb_data["photo_page"] = photo_page - 1

            await admin_see_photos_client(call, cb_data)
        else:
            await call.answer("Должно быть минимум 1 фото")

    elif value == "insert_photo":
        if len(client.photo) < 10:
            await call.answer()
            msg = await call.message.answer("Отправьте фото.")
            await AdminChangeClient.Photo.set()
            async with state.proxy() as data:
                data["photo_page"] = photo_page
                data["call"] = call
                data["callback_data"] = callback_data
            await sleep(time_sleep)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        else:
            await call.answer("Больше 10 фото быть не может")


async def load_admin_change_photo_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        call = data.get("call")
        callback_data = data.get("callback_data")
        client_id = int(callback_data.get("user_id"))
        await commands.append_user_photo(user_id=client_id, new_photo=message.photo[0].file_id)
        await message.delete()
        await admin_see_photos_client(call, callback_data)
        await state.finish()


async def admin_change_location_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Отправьте местоположение(возможно только с мобильного устройства)")
    await AdminChangeClient.Location.set()
    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_location_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        location = message.location
        latitude = location.latitude
        longitude = location.longitude
        await commands.update_user_latitude(client_id, latitude)
        await commands.update_user_longitude(client_id, longitude)
        msg = await message.answer("Местоположение пользователя изменено")

        await start_admin_change_settings_client(message, callback_data)
        await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)


async def admin_change_search_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    kb = get_search_gender_kb(params=["base"])
    await call.message.delete()
    await call.message.answer("Выберите кого будет искать пользователь", reply_markup=kb)
    await AdminChangeClient.SearchGender.set()
    async with state.proxy() as data:
        data["callback_data"] = callback_data


async def load_admin_change_search_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_search_gender(user_id=client_id, search_gender=gender)
        await start_admin_change_settings_client(call, callback_data)
        await state.finish()


async def admin_change_search_age_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите два числа - диапозон поиска")
    await AdminChangeClient.SearchAge.set()
    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_search_age_client(message: types.Message, state: FSMContext):
    msg_text = message.text.split()
    m_t = "".join(msg_text)
    if m_t.isdigit() and len(msg_text) == 2:
        async with state.proxy() as data:
            callback_data = data["callback_data"]
            client_id = int(callback_data.get("user_id"))
            msg_text = sorted([int(msg_text[0]), int(msg_text[1])])
            await commands.update_user_search_age(user_id=client_id, search_age=msg_text)
            msg = await message.answer(f"У пользователя установлен новый диапозон поиска: {msg_text}")

            await start_admin_change_settings_client(message, callback_data)
            await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)
    else:
        msg = await message.answer("Введите два числа - диапозон поиска")
        await sleep_bot_delete_msg_message_delete(msg, message)


async def admin_change_search_location_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Отправьте местоположение поиска(возможно только с мобильного устройства)")
    await AdminChangeClient.SearchLocation.set()
    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_search_location_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        location = message.location
        latitude = location.latitude
        longitude = location.longitude
        await commands.update_user_search_latitude(client_id, latitude)
        await commands.update_user_search_longitude(client_id, longitude)
        msg = await message.answer("Местоположение изменено")

        await start_admin_change_settings_client(message, callback_data)
        await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)


async def admin_change_search_radius_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите радиус поиска одним числом в километрах")
    await AdminChangeClient.SearchRadius.set()
    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


async def load_admin_change_search_radius_client(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            callback_data = data["callback_data"]
            client_id = int(callback_data.get("user_id"))
            await commands.update_user_search_radius(user_id=client_id, search_radius=int(message.text))
            msg = await message.answer(f"У пользователя установлен новый радиус поиска: {message.text}")

            await start_admin_change_settings_client(message, callback_data)
            await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)
    else:
        msg = await message.answer("Введите радиус поиска одним числом в километрах")

        await sleep_bot_delete_msg_message_delete(msg, message)


def register_admin_change_settings_client_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_admin_change_settings_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_set_clt"))
    dp.register_message_handler(start_admin_change_settings_client, IsSuperAdmin() | IsAdmin(),
                                text="admin_change_settings_client")
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_name_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_name"))
    dp.register_message_handler(load_admin_change_name_client, IsSuperAdmin() | IsAdmin(), state=AdminChangeClient.Name)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_age_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_age"))
    dp.register_message_handler(load_admin_change_age_client, IsSuperAdmin() | IsAdmin(), state=AdminChangeClient.Age)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_gender_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_gender"))
    dp.register_callback_query_handler(load_admin_change_gender_client, IsSuperAdmin() | IsAdmin(),
                                       gender_callback.filter(), state=AdminChangeClient.Gender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_biography_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_biography"))
    dp.register_message_handler(load_admin_change_biography_client, IsSuperAdmin() | IsAdmin(),
                                state=AdminChangeClient.Biography)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_location_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_loc"))
    dp.register_message_handler(load_admin_change_location_client, IsSuperAdmin() | IsAdmin(),
                                content_types=types.ContentTypes.LOCATION, state=AdminChangeClient.Location)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_gender_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_sch_gender"))
    dp.register_callback_query_handler(load_admin_change_search_gender_client, IsSuperAdmin() | IsAdmin(),
                                       gender_callback.filter(), state=AdminChangeClient.SearchGender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_age_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_sch_age"))
    dp.register_message_handler(load_admin_change_search_age_client, IsSuperAdmin() | IsAdmin(),
                                state=AdminChangeClient.SearchAge)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_location_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_sch_loc"))
    dp.register_message_handler(load_admin_change_search_location_client, IsSuperAdmin() | IsAdmin(),
                                content_types=types.ContentTypes.LOCATION, state=AdminChangeClient.SearchLocation)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_radius_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_sch_radius"))
    dp.register_message_handler(load_admin_change_search_radius_client, IsSuperAdmin() | IsAdmin(),
                                state=AdminChangeClient.SearchRadius)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_see_first_photo_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="chg_clt_photo"))
    dp.register_callback_query_handler(admin_see_photos_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter(value="value"))
    dp.register_callback_query_handler(admin_change_photo_client, IsSuperAdmin() | IsAdmin(),
                                       change_user_card_callback.filter())
    dp.register_message_handler(load_admin_change_photo_client, IsSuperAdmin() | IsAdmin(),
                                content_types=['photo'], state=AdminChangeClient.Photo)
