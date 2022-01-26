from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands import common_commands_users_db as commands
from tg_bot.filters import IsSuperAdminOrAdminOrModerOrClient
from tg_bot.handlers.templetes_handlers.tmp_card_user import see_card
from tg_bot.handlers.templetes_handlers.tmp_change_settings import change_photo_user
from tg_bot.handlers.templetes_handlers.tmp_misc import sleep_bot_delete_msg_message_delete, sleep_bot_del_msg, \
    get_self_caption_users, \
    welcome_cap, welcome_block_call, welcome_block_message, get_self_caption_for_change_photo_users
from tg_bot.keyboards.all_users.inline.all_users import get_gender_kb, get_search_gender_kb
from tg_bot.keyboards.all_users.inline.all_users_change_self_settings import get_settings_user_kb, get_user_photo_kb
from tg_bot.keyboards.callback_datas.cb_datas import change_user_callback, gender_callback, user_card_callback
from tg_bot.misc.user_status import status_user
from tg_bot.states.user_states import Change

"""Мои настройки в Меню в роли клиента. У клиента соответственно это главное меню."""


# change_settings выводит клавиатуру для изменения настроек пользователя,
# обработка кнопки - Мои настройки в меню в роли клиента
async def change_settings(msg: Union[types.CallbackQuery, types.Message]):
    user_status = await status_user(msg)
    kb = get_settings_user_kb(user_status)

    welcome_text = await welcome_cap(msg)

    if type(msg) == types.CallbackQuery:
        await welcome_block_call(msg, kb, welcome_text)
    else:
        await welcome_block_message(msg, kb, welcome_text)


# change_name - выводит приглашение на ввод нового имени пользователя
async def change_name(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите ваше новое имя")
    await Change.Name.set()

    await sleep_bot_del_msg(msg)


# load_change_name загружаем новое имя пользователю
async def load_change_name(message: types.Message, state: FSMContext):
    await commands.update_user_name(user_id=message.from_user.id, name=message.text)
    msg = await message.answer(f"У пользователя {message.from_user.username} установлено новое имя: {message.text}")
    await state.finish()

    await sleep_bot_delete_msg_message_delete(msg, message)


# change_age - выводит приглашение на ввод нового возраста пользователя
async def change_age(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите возраст")
    await Change.Age.set()

    await sleep_bot_del_msg(msg)


# load_change_age загружаем новый возраст пользователю
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


# change_gender - выводит инлайн клавиатуру на ввод нового пола пользователя
async def change_gender(call: types.CallbackQuery):
    kb = get_gender_kb(params=("base",))
    await call.message.delete()
    await call.message.answer("Выберите кто вы", reply_markup=kb)
    await Change.Gender.set()


# load_change_gender загружаем новый пол пользователю
async def load_change_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    await commands.update_user_gender(user_id=call.from_user.id, gender=gender)
    await state.finish()
    await change_settings(call)


# change_biography - выводит приглашение на ввод новой биографии пользователя
async def change_biography(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Напишите о себе")
    await Change.Biography.set()

    await sleep_bot_del_msg(msg)


# load_change_biography загружаем новую биографию пользователю
async def load_change_biography(message: types.Message, state: FSMContext):
    await commands.update_user_biography(user_id=message.from_user.id, biography=message.text)
    msg = await message.answer(f"{message.from_user.username}: {message.text}")
    await state.finish()

    await sleep_bot_delete_msg_message_delete(msg, message)


# see_first_photo - выводит инлайн клавиатуру с первым фото пользователя
async def see_first_photo(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    user_photo = user.photo

    user_status = await status_user(call)
    kb = get_user_photo_kb(user_status=user_status, category="all_users", page=1, photo_page=1,
                           user_id=call.from_user.id, user_photo=user_photo)

    caption = await get_self_caption_for_change_photo_users(user)

    await call.message.delete()
    if user.photo:
        await call.message.answer_photo(photo=user.photo[0], caption=caption, reply_markup=kb)
    else:
        await call.message.answer(text=caption, reply_markup=kb)


# see_photos - просмотр фото пользователя через инлайн клавиатуру
async def see_photos(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, params=("change_settings",), func_get_caption=get_self_caption_users)


# change_photo - изменение фото пользователя через инлайн клавиатуру
async def change_photo(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await change_photo_user(call, callback_data, state, func_see_photos=see_photos, IsUserSt=Change)


# load_change_photo - добавляем фото в конец списка
async def load_change_photo(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    async with state.proxy() as data:
        call = data.get("call")
        callback_data = data.get("callback_data")
        await commands.append_user_photo(user_id=user.user_id, new_photo=message.photo[0].file_id)
        await message.delete()
        await see_photos(call, callback_data)
        await state.finish()


# change_location - отправляет предложение ввести новое местоположение
async def change_location(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Отправьте свое местоположение(возможно только с мобильного устройства)")
    await Change.Location.set()

    await sleep_bot_del_msg(msg)


# load_change_location - записывает новое местоположение пользователя
async def load_change_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await commands.update_user_latitude(message.from_user.id, latitude)
    await commands.update_user_longitude(message.from_user.id, longitude)

    await state.finish()
    await message.delete()


# change_search_gender - отправляет предложение ввести новый пол для поиска
async def change_search_gender(call: types.CallbackQuery):
    kb = get_search_gender_kb(params=("base",))
    await call.message.delete()
    await call.message.answer("Выберите кого вы ищите", reply_markup=kb)
    await Change.SearchGender.set()


# load_change_search_gender - записывает новый пол для поиска
async def load_change_search_gender(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    await commands.update_user_search_gender(user_id=call.from_user.id, search_gender=gender)
    await state.finish()
    await change_settings(call)


# change_search_age - отправляет предложение ввести новый диапозон возраста для поиска
async def change_search_age(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите два числа - диапозон поиска")
    await Change.SearchAge.set()

    await sleep_bot_del_msg(msg)


# load_change_search_age - записывает новый диапозон возраста для поиска
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


# change_search_location - отправляет предложение ввести новое местоположение для поиска
async def change_search_location(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Отправьте местоположение поиска(возможно только с мобильного устройства)")
    await Change.SearchLocation.set()

    await sleep_bot_del_msg(msg)


# load_change_search_location - записывает новое местоположение пользователя для поиска
async def load_change_search_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await commands.update_user_search_latitude(message.from_user.id, latitude)
    await commands.update_user_search_longitude(message.from_user.id, longitude)

    await state.finish()
    await message.delete()


# change_search_radius - отправляет предложение ввести новый радиус для поиска
async def change_search_radius(call: types.CallbackQuery):
    await call.answer()
    msg = await call.message.answer("Введите радиус поиска одним числом в километрах")
    await Change.SearchRadius.set()

    await sleep_bot_del_msg(msg)


# load_change_search_radius - записывает новый радиус для поиска
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
    dp.register_callback_query_handler(change_settings, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="srt_ch_set"))
    dp.register_message_handler(change_settings, IsSuperAdminOrAdminOrModerOrClient(),
                                text="start_change_settings")
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_name, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="name"))
    dp.register_message_handler(load_change_name, IsSuperAdminOrAdminOrModerOrClient(),
                                state=Change.Name)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_age, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="age"))
    dp.register_message_handler(load_change_age, IsSuperAdminOrAdminOrModerOrClient(),
                                state=Change.Age)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_gender, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="gender"))
    dp.register_callback_query_handler(load_change_gender, IsSuperAdminOrAdminOrModerOrClient(),
                                       gender_callback.filter(), state=Change.Gender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_biography, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="biography"))
    dp.register_message_handler(load_change_biography, IsSuperAdminOrAdminOrModerOrClient(),
                                state=Change.Biography)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(see_first_photo, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="photo"))
    dp.register_callback_query_handler(see_photos, IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="all_users", value="value"))
    dp.register_callback_query_handler(change_photo, IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="all_users"))
    dp.register_message_handler(load_change_photo, IsSuperAdminOrAdminOrModerOrClient(),
                                content_types=['photo'], state=Change.Photo)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_location, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="loc"))
    dp.register_message_handler(load_change_location, IsSuperAdminOrAdminOrModerOrClient(),
                                content_types=types.ContentTypes.LOCATION, state=Change.Location)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_gender, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="s_gender"))
    dp.register_callback_query_handler(load_change_search_gender, IsSuperAdminOrAdminOrModerOrClient(),
                                       gender_callback.filter(), state=Change.SearchGender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_age, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="s_age"))
    dp.register_message_handler(load_change_search_age, IsSuperAdminOrAdminOrModerOrClient(),
                                state=Change.SearchAge)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_location, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="s_loc"))
    dp.register_message_handler(load_change_search_location, IsSuperAdminOrAdminOrModerOrClient(),
                                content_types=types.ContentTypes.LOCATION, state=Change.SearchLocation)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(change_search_radius, IsSuperAdminOrAdminOrModerOrClient(),
                                       change_user_callback.filter(param="s_radius"))
    dp.register_message_handler(load_change_search_radius, IsSuperAdminOrAdminOrModerOrClient(),
                                state=Change.SearchRadius)
