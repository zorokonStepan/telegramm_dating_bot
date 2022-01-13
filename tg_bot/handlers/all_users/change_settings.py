from asyncio import sleep
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from create_bot import bot
from config import time_sleep
from tg_bot.database.schemas.users_commands import common_commands_users_db as commands
from tg_bot.filters import IsSuperAdmin, IsAdmin, IsModerator, IsClient
from tg_bot.keyboards.all_users.inline.all_users import get_gender_kb, get_search_gender_kb
from tg_bot.keyboards.all_users.inline.all_users_change_self_settings import get_settings_user_kb, get_user_photo_kb

from tg_bot.keyboards.callback_datas.cb_datas import change_user_callback, gender_callback, user_card_callback
from tg_bot.states.state_change import Change

from tg_bot.misc.for_handlers import sleep_bot_delete_msg_message_delete, sleep_bot_del_msg
from tg_bot.misc.user_status import status_user


async def change_settings(msg: Union[types.CallbackQuery, types.Message]):
    user_status = await status_user(msg)
    kb = get_settings_user_kb(user_status)

    if type(msg) == types.CallbackQuery:
        try:
            await msg.message.edit_text(text=f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}",
                                        reply_markup=kb)
        except BadRequest:
            await msg.message.delete()
            await msg.message.answer(text=f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}",
                                     reply_markup=kb)
    else:
        await msg.answer(text=f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}", reply_markup=kb)


async def change_name(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите ваше новое имя")
    await Change.Name.set()

    await sleep_bot_del_msg(msg)


async def load_change_name(message: types.Message, state: FSMContext):
    await commands.update_user_name(user_id=message.from_user.id, name=message.text)
    msg = await message.answer(f"У пользователя {message.from_user.username} установлено новое имя: {message.text}")
    await state.finish()

    await sleep_bot_delete_msg_message_delete(msg, message)


async def change_age(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите возраст")
    await Change.Age.set()

    await sleep_bot_del_msg(msg)


async def load_change_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await commands.update_user_age(user_id=message.from_user.id, age=int(message.text))
        msg = await message.answer(
            f"У пользователя {message.from_user.username} установлен новый возраст: {message.text}")
        await state.finish()

        await sleep_bot_delete_msg_message_delete(msg, message)

    else:
        msg = await message.answer("Введите возраст одним числом")

        await sleep_bot_delete_msg_message_delete(msg, message)


async def change_gender(call: types.CallbackQuery):
    kb = get_gender_kb(params=["base"])
    await call.message.delete()
    await call.message.answer("Выберите кто вы", reply_markup=kb)
    await Change.Gender.set()


async def load_change_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    await commands.update_user_gender(user_id=call.from_user.id, gender=gender)
    await state.finish()
    await change_settings(call)


async def change_biography(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Напишите о себе")
    await Change.Biography.set()

    await sleep_bot_del_msg(msg)


async def load_change_biography(message: types.Message, state: FSMContext):
    await commands.update_user_biography(user_id=message.from_user.id, biography=message.text)
    msg = await message.answer(f"{message.from_user.username}: {message.text}")
    await state.finish()

    await sleep_bot_delete_msg_message_delete(msg, message)


async def see_first_photo(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    user_photo = user.photo

    user_status = await status_user(call)
    kb = get_user_photo_kb(user_status=user_status, category="all_users", page=1, photo_page=1,
                           user_id=call.from_user.id, user_photo=user_photo)
    caption = "Вы можете удалить или добавить фотографии. Фотографий не может быть меньше 1 шт и больше 10 шт"

    await call.message.delete()
    await call.message.answer_photo(photo=user.photo[0], caption=caption, reply_markup=kb)


async def see_photos(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await commands.select_user(user_id)

    # id для отладки - удалить
    caption = f"Фотографий не может быть меньше 1 шт и больше 10 шт\n" \
              f"{user.user_id=} Мое имя: {user.name}, мне: {user.age}, @{user.username}.\n{user.biography}"
    user_status = await status_user(call)
    kb = get_user_photo_kb(user_status=user_status, user_id=user.user_id, user_photo=user.photo, page=page,
                           photo_page=photo_page, category=category)

    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    await call.message.edit_media(media=photo, reply_markup=kb)


async def change_photo(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    value = callback_data.get("value")
    user = await commands.select_user(user_id)

    if value == "delete_photo":
        if len(user.photo) > 1:
            await call.answer()
            await commands.delete_user_photo(user_id=user_id, index_delete_photo=photo_page - 1)
            cb_data = callback_data
            # чтобы не выходить за index out of range
            if photo_page == 1:
                cb_data["photo_page"] = photo_page
            else:
                cb_data["photo_page"] = photo_page - 1

            await see_photos(call, cb_data)
        else:
            await call.answer("Должно быть минимум 1 фото")

    elif value == "insert_photo":
        if len(user.photo) < 10:
            await call.answer()
            msg = await call.message.answer("Отправьте фото.")
            await Change.Photo.set()
            async with state.proxy() as data:
                data["photo_page"] = photo_page
                data["call"] = call
                data["callback_data"] = callback_data
            await sleep(time_sleep)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        else:
            await call.answer("Больше 10 фото быть не может")


async def load_change_photo(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    async with state.proxy() as data:
        call = data.get("call")
        callback_data = data.get("callback_data")
        await commands.append_user_photo(user_id=user.user_id, new_photo=message.photo[0].file_id)
        await message.delete()
        await see_photos(call, callback_data)
        await state.finish()


async def change_location(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Отправьте свое местоположение(возможно только с мобильного устройства)")
    await Change.Location.set()

    await sleep_bot_del_msg(msg)


async def load_change_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await commands.update_user_latitude(message.from_user.id, latitude)
    await commands.update_user_longitude(message.from_user.id, longitude)

    await state.finish()
    await message.delete()


async def change_search_gender(call: types.CallbackQuery):
    kb = get_search_gender_kb(params=["base"])
    await call.message.delete()
    await call.message.answer("Выберите кого вы ищите", reply_markup=kb)
    await Change.SearchGender.set()


async def load_change_search_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    await commands.update_user_search_gender(user_id=call.from_user.id, search_gender=gender)
    await state.finish()
    await change_settings(call)


async def change_search_age(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите два числа - диапозон поиска")
    await Change.SearchAge.set()

    await sleep_bot_del_msg(msg)


async def load_change_search_age(message: types.Message, state: FSMContext):
    msg_text = message.text.split()
    m_t = "".join(msg_text)
    if m_t.isdigit() and len(msg_text) == 2:
        msg_text = sorted([int(msg_text[0]), int(msg_text[1])])
        await commands.update_user_search_age(user_id=message.from_user.id, search_age=msg_text)
        msg = await message.answer(
            f"У пользователя {message.from_user.username} установлен новый диапозон поиска: {msg_text}")
        await state.finish()

        await sleep_bot_delete_msg_message_delete(msg, message)
    else:
        msg = await message.answer("Введите два числа - диапозон поиска")

        await sleep_bot_delete_msg_message_delete(msg, message)


async def change_search_location(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Отправьте местоположение поиска(возможно только с мобильного устройства)")
    await Change.SearchLocation.set()

    await sleep_bot_del_msg(msg)


async def load_change_search_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await commands.update_user_search_latitude(message.from_user.id, latitude)
    await commands.update_user_search_longitude(message.from_user.id, longitude)

    await state.finish()
    await message.delete()


async def change_search_radius(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите радиус поиска одним числом в километрах")
    await Change.SearchRadius.set()

    await sleep_bot_del_msg(msg)


async def load_change_search_radius(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await commands.update_user_search_radius(user_id=message.from_user.id, search_radius=int(message.text))
        msg = await message.answer(
            f"У пользователя {message.from_user.username} установлен новый радиус поиска: {message.text}")
        await state.finish()

        await sleep_bot_delete_msg_message_delete(msg, message)
    else:
        msg = await message.answer("Введите радиус поиска одним числом в километрах")

        await sleep_bot_delete_msg_message_delete(msg, message)


def register_change_settings_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(change_settings, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="start_change_settings"))
    dp.register_message_handler(change_settings, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                text="start_change_settings")
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_name, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="name"))
    dp.register_message_handler(load_change_name, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                state=Change.Name)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_age, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="age"))
    dp.register_message_handler(load_change_age, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                state=Change.Age)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_gender, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="gender"))
    dp.register_callback_query_handler(load_change_gender, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       gender_callback.filter(), state=Change.Gender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_biography, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="biography"))
    dp.register_message_handler(load_change_biography, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                state=Change.Biography)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(see_first_photo, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="photo"))
    dp.register_callback_query_handler(see_photos, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       user_card_callback.filter(category="all_users", value="value"))
    dp.register_callback_query_handler(change_photo, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       user_card_callback.filter(category="all_users"))
    dp.register_message_handler(load_change_photo, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                content_types=['photo'], state=Change.Photo)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_location, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="location"))
    dp.register_message_handler(load_change_location, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                content_types=types.ContentTypes.LOCATION, state=Change.Location)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_gender, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="search_gender"))
    dp.register_callback_query_handler(load_change_search_gender, IsSuperAdmin() | IsAdmin() | IsModerator() |
                                       IsClient(), gender_callback.filter(), state=Change.SearchGender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_age, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="search_age"))
    dp.register_message_handler(load_change_search_age, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                state=Change.SearchAge)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_location, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="search_location"))
    dp.register_message_handler(load_change_search_location, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                content_types=types.ContentTypes.LOCATION, state=Change.SearchLocation)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_radius, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                       change_user_callback.filter(param="search_radius"))
    dp.register_message_handler(load_change_search_radius, IsSuperAdmin() | IsAdmin() | IsModerator() | IsClient(),
                                state=Change.SearchRadius)
