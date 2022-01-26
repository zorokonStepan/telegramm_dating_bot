from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands import common_commands_users_db as commands
from tg_bot.filters import IsSuperAdminOrAdmin
from tg_bot.handlers.templetes_handlers.tmp_card_user import see_card
from tg_bot.handlers.templetes_handlers.tmp_change_settings import change_photo_user
from tg_bot.handlers.templetes_handlers.tmp_misc import state_finish_sleep_bot_del_msg_message_delete, \
    sleep_bot_delete_msg_message_delete, state_save_data_sleep_bot_delete_msg, get_caption_for_managers, \
    welcome_block_call, welcome_block_message
from tg_bot.keyboards.all_users.inline.all_users import get_gender_kb, get_search_gender_kb
from tg_bot.keyboards.callback_datas.cb_datas import gender_callback, change_user_card_callback
from tg_bot.keyboards.manager.inline.change_settings_client import get_change_settings_client_kb, \
    get_change_client_photo_kb
from tg_bot.misc.user_status import status_user
from tg_bot.states.user_states import AdminChangeClient

"""В этом модуле все обработчики для изменения настроек администраторами
***********************************************************************************************************************
чтобы вернуться на страницу пользователя у которого меняются настройки используется схема:

в callback_query_handler сохраняется callback_data
    async with state.proxy() as data:
        data["callback_data"] = callback_data
        
а в message_handler callback_data достается из state.proxy()
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))"""


# start_admin_change_settings_client выводит клавиатуру для изменения настроек пользователя,
# обработка кнопки - изменить данные пользователя
async def start_admin_change_settings_client(msg: Union[types.CallbackQuery, types.Message], callback_data: dict):
    user_status = await status_user(msg)
    category = callback_data.get("category")
    page = int(callback_data.get("page"))
    photo_page = int(callback_data.get("photo_page"))
    client_id = int(callback_data.get("user_id"))

    kb = get_change_settings_client_kb(user_status=user_status, category=category, page=page,
                                       photo_page=photo_page, user_id=client_id)

    welcome_text = "Меню для изменения настроек пользователя"

    if type(msg) == types.CallbackQuery:
        await welcome_block_call(msg, kb, welcome=welcome_text)
    else:
        await welcome_block_message(msg, kb, welcome=welcome_text)


# admin_change_name_client - выводит приглашение на ввод нового имени пользователя
async def admin_change_name_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите новое имя пользователя")
    await AdminChangeClient.Name.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_name_client загружаем новое имя пользователю
async def load_admin_change_name_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_name(user_id=client_id, name=message.text)
        msg = await message.answer(f"У пользователя установлено новое имя: {message.text}")

        await start_admin_change_settings_client(message, callback_data)
        await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)


# admin_change_age_client - выводит приглашение на ввод нового возраста пользователя
async def admin_change_age_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите возраст")
    await AdminChangeClient.Age.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_age_client загружаем новый возраст пользователю
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


# admin_change_gender_client - выводит инлайн клавиатуру на ввод нового пола пользователя
async def admin_change_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    kb = get_gender_kb(params=("base",))
    await call.message.delete()
    await call.message.answer("Выберите пол пользователя", reply_markup=kb)
    await AdminChangeClient.Gender.set()
    async with state.proxy() as data:
        data["callback_data"] = callback_data


# load_admin_change_gender_client загружаем новый пол пользователю
async def load_admin_change_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_gender(user_id=client_id, gender=gender)
        await start_admin_change_settings_client(call, callback_data)
        await state.finish()


# admin_change_biography_client - выводит приглашение на ввод новой биографии пользователя
async def admin_change_biography_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Напишите биографию пользователя")
    await AdminChangeClient.Biography.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_biography_client загружаем новую биографию пользователю
async def load_admin_change_biography_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_biography(user_id=client_id, biography=message.text)
        msg = await message.answer(f"У пользователя новая биография: {message.text}")

        await start_admin_change_settings_client(message, callback_data)
        await state_finish_sleep_bot_del_msg_message_delete(message, state, msg)


# admin_see_first_photo_client - выводит инлайн клавиатуру с первым фото пользователя
async def admin_see_first_photo_client(call: types.CallbackQuery, callback_data: dict):
    client_id = int(callback_data.get("user_id"))
    category = callback_data.get("category")
    client = await commands.select_user(client_id)
    client_photo = client.photo

    user_status = await status_user(call)
    kb = get_change_client_photo_kb(user_status=user_status, category=category, page=1, photo_page=1,
                                    user_id=client_id, user_photo=client_photo)

    caption = await get_caption_for_managers(client)

    await call.message.delete()
    if client.photo:
        await call.message.answer_photo(photo=client.photo[0], caption=caption, reply_markup=kb)
    else:
        await call.message.answer(text=caption, reply_markup=kb)


# admin_see_photos_client - просмотр фото пользователя через инлайн клавиатуру
async def admin_see_photos_client(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, params=("admin_change_settings_client",),
                   func_get_caption=get_caption_for_managers)


# admin_change_photo_client - изменение фото пользователя через инлайн клавиатуру
async def admin_change_photo_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await change_photo_user(call, callback_data, state, func_see_photos=admin_see_photos_client,
                            IsUserSt=AdminChangeClient)


# load_admin_change_photo_client - добавляем фото в конец списка
async def load_admin_change_photo_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        call = data.get("call")
        callback_data = data.get("callback_data")
        client_id = int(callback_data.get("user_id"))
        await commands.append_user_photo(user_id=client_id, new_photo=message.photo[0].file_id)
        await message.delete()
        await admin_see_photos_client(call, callback_data)
        await state.finish()


# admin_change_location_client - отправляет предложение ввести новое местоположение
async def admin_change_location_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Отправьте местоположение(возможно только с мобильного устройства)")
    await AdminChangeClient.Location.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_location_client - записывает новое местоположение пользователя
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


# admin_change_search_gender_client - отправляет предложение ввести новый пол для поиска
async def admin_change_search_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    kb = get_search_gender_kb(params=("base",))
    await call.message.delete()
    await call.message.answer("Выберите кого будет искать пользователь", reply_markup=kb)
    await AdminChangeClient.SearchGender.set()
    async with state.proxy() as data:
        data["callback_data"] = callback_data


# load_admin_change_search_gender_client - записывает новый пол для поиска
async def load_admin_change_search_gender_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    gender = callback_data.get("gender")
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        await commands.update_user_search_gender(user_id=client_id, search_gender=gender)

        await start_admin_change_settings_client(call, callback_data)
        await state.finish()


# admin_change_search_age_client - отправляет предложение ввести новый диапозон возраста для поиска
async def admin_change_search_age_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите два числа - диапозон поиска")
    await AdminChangeClient.SearchAge.set()
    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_search_age_client - записывает новый диапозон возраста для поиска
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


# admin_change_search_location_client - отправляет предложение ввести новое местоположение для поиска
async def admin_change_search_location_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Отправьте местоположение поиска(возможно только с мобильного устройства)")
    await AdminChangeClient.SearchLocation.set()

    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_search_location_client - записывает новое местоположение пользователя для поиска
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


# admin_change_search_radius_client - отправляет предложение ввести новый радиус для поиска
async def admin_change_search_radius_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите радиус поиска одним числом в километрах")
    await AdminChangeClient.SearchRadius.set()
    await state_save_data_sleep_bot_delete_msg(state, callback_data, msg)


# load_admin_change_search_radius_client - записывает новый радиус для поиска
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
    dp.register_callback_query_handler(start_admin_change_settings_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_set_clt"))
    dp.register_message_handler(start_admin_change_settings_client, IsSuperAdminOrAdmin(),
                                text="admin_change_settings_client")
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_name_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_name"))
    dp.register_message_handler(load_admin_change_name_client, IsSuperAdminOrAdmin(), state=AdminChangeClient.Name)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_age_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_age"))
    dp.register_message_handler(load_admin_change_age_client, IsSuperAdminOrAdmin(), state=AdminChangeClient.Age)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_gender_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_gend"))
    dp.register_callback_query_handler(load_admin_change_gender_client, IsSuperAdminOrAdmin(),
                                       gender_callback.filter(), state=AdminChangeClient.Gender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_biography_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_braphy"))
    dp.register_message_handler(load_admin_change_biography_client, IsSuperAdminOrAdmin(),
                                state=AdminChangeClient.Biography)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_location_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_loc"))
    dp.register_message_handler(load_admin_change_location_client, IsSuperAdminOrAdmin(),
                                content_types=types.ContentTypes.LOCATION, state=AdminChangeClient.Location)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_gender_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_s_gend"))
    dp.register_callback_query_handler(load_admin_change_search_gender_client, IsSuperAdminOrAdmin(),
                                       gender_callback.filter(), state=AdminChangeClient.SearchGender)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_age_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_s_age"))
    dp.register_message_handler(load_admin_change_search_age_client, IsSuperAdminOrAdmin(),
                                state=AdminChangeClient.SearchAge)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_location_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_s_loc"))
    dp.register_message_handler(load_admin_change_search_location_client, IsSuperAdminOrAdmin(),
                                content_types=types.ContentTypes.LOCATION, state=AdminChangeClient.SearchLocation)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_change_search_radius_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_s_rad"))
    dp.register_message_handler(load_admin_change_search_radius_client, IsSuperAdminOrAdmin(),
                                state=AdminChangeClient.SearchRadius)
    # -------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_see_first_photo_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="chg_c_ph"))
    dp.register_callback_query_handler(admin_see_photos_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter(value="value"))
    dp.register_callback_query_handler(admin_change_photo_client, IsSuperAdminOrAdmin(),
                                       change_user_card_callback.filter())
    dp.register_message_handler(load_admin_change_photo_client, IsSuperAdminOrAdmin(),
                                content_types=['photo'], state=AdminChangeClient.Photo)
