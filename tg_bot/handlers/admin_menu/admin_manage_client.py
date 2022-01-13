import asyncio
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest, ChatNotFound

from create_bot import bot
from config import COUNT_USERS_CARDS_AT_PAGE, TIME_BANNED, time_sleep
from tg_bot.database.schemas.book_complaints_commands.commands_book_complaints_db import add_record
from tg_bot.database.schemas.users_commands.client_commands_users_db import select_states_clients, update_state_client, \
    unbanned_client, banned_all_time_client, banned_at_time_client
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, delete_user, select_all_users
from tg_bot.filters import IsAdmin, IsSuperAdmin
from tg_bot.handlers.admin_menu.admin_change_settings_client import start_admin_change_settings_client
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_admin, start_main_menu_super_admin
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback
from tg_bot.keyboards.manager.inline.get_card import admin_and_super_admin_get_card_client_kb
from tg_bot.misc.splitting_list_parts import func_chunks_generators


async def search_all_clients(call: types.CallbackQuery, callback_data: dict):
    all_clients = await select_states_clients("wait_client", "client", "banned_client")

    if all_clients:
        all_clients_cards = list(func_chunks_generators(all_clients, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(all_clients_cards):
            page = len(all_clients_cards)

        category = callback_data.get("category")
        user_status = await status_user(call)
        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=all_clients_cards, page=page,
                                       category=category, wait_client=True)
        try:
            await call.message.edit_text(text=f"Добро пожаловать в Бот Знакомств, {call.from_user.full_name}",
                                         reply_markup=kb)
        except BadRequest:
            chat_id = call.from_user.id
            await call.message.delete()
            await bot.send_message(chat_id=chat_id,
                                   text=f"Добро пожаловать в Бот Знакомств, {call.from_user.full_name}",
                                   reply_markup=kb)
    else:
        await call.answer('Список пуст')


async def see_card_client(msg: Union[types.CallbackQuery, types.Message], callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    # вся информация о клиенте кроме {user.time_banned=}
    # иначе -> aiogram.utils.exceptions.BadRequest: Media_caption_too_long
    caption = f"{user.client_state=}\n, @{user.username}, {user.name=}, {user.age=} ." \
              f"{user.user_id=}, {user.gender=}, {user.latitude=}, {user.longitude=}" \
              f"{user.search_gender=}, {user.search_age=}, {user.search_latitude=}, {user.search_longitude}," \
              f"{user.search_radius=}\n{user.biography=}"

    user_status = await status_user(msg)
    kb = admin_and_super_admin_get_card_client_kb(user_id=user.user_id, user_photo=user.photo,
                                                  page=page, user_status=user_status,
                                                  photo_page=photo_page, category=category)

    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    if type(msg) == types.CallbackQuery:
        try:
            await msg.message.edit_media(media=photo, reply_markup=kb)
        except BadRequest:
            await msg.message.delete()
            await msg.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)
    else:
        try:
            await msg.edit_media(media=photo, reply_markup=kb)
        except BadRequest:
            await msg.delete()
            await msg.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)


async def moderation_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    client_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    manager = await select_user(call.from_user.id)
    client = await select_user(client_id)

    if value == "admin_banned_user_time":
        if client.client_state == "client":
            await call.answer()
            # ЗАБАНИТЬ НА ВРЕМЯ
            await banned_at_time_client(user_id=client_id)
            await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                             banned_user_id=client_id, banned_username=client.username)
            await see_card_client(call, callback_data)

            try:
                await bot.send_message(chat_id=client_id, text=f"Вы забанены на {TIME_BANNED} часов")
            except ChatNotFound:
                pass

        elif client.client_state == "banned_client":
            await call.answer("Пользователь уже забанен. Разбаньте его и забаньте снова.")

        else:
            await call.answer("Доступно только для client")

    elif value == "admin_banned_user_all_time":
        if client.client_state == "client":
            await call.answer()
            await banned_all_time_client(user_id=client_id)
            await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                             banned_user_id=client_id, banned_username=client.username)
            await see_card_client(call, callback_data)

            try:
                await bot.send_message(chat_id=client_id, text="Вы забанены навсегда")
            except ChatNotFound:
                pass

        elif client.client_state == "banned_client":
            await call.answer("Пользователь уже забанен. Разбаньте его и забаньте снова.")

        else:
            await call.answer("Доступно только для client")

    elif value == "admin_unbanned_user":
        if client.client_state == "banned_client":
            await call.answer()
            await unbanned_client(user_id=client_id)
            await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                             banned_user_id=client_id, banned_username=client.username)
            await see_card_client(call, callback_data)

            try:
                await bot.send_message(chat_id=client_id, text="Вы разбанены")
            except ChatNotFound:
                pass
        else:
            await call.answer("Доступно только для забаненных пользователей")

    # если все в порядке, то меняем состояние клиента на client и он сможет пользоваться ботом
    elif value == "moderation_true":
        if client.client_state == "wait_client":
            await call.answer()
            await update_state_client(user_id=client_id, client_state="client")
            # чтобы сразу увидеть изменения состояния клиента
            await see_card_client(call, callback_data)

            try:
                await bot.send_message(chat_id=client_id, text="Ваша анкета прошла проверку. Можете пользоваться ботом")
            except ChatNotFound:
                pass
        else:
            await call.answer("Доступно только для пользователей ожидающих модерацию")

    # если не все в порядке, то сообщаем об этом пользователю и удаляем его из БД
    elif value == "moderation_false":
        if client.client_state == "wait_client":
            await call.answer()
            try:
                await bot.send_message(chat_id=client_id,
                                       text="Ваша анкета не прошла проверку. Можете заполнить ее снова")
            except ChatNotFound:
                pass
            await delete_user(user_id=client_id)

            all_clients = await select_states_clients("wait_client", "client", "banned_client")
            if all_clients:
                await search_all_clients(call, callback_data)
            else:
                user_status = await status_user(call)
                if user_status == "admin":
                    await start_main_menu_admin(call)
                elif user_status == "super_admin":
                    await start_main_menu_super_admin(call)

        else:
            await call.answer("Доступно только для пользователей ожидающих модерацию")

    elif value == "send_message_as_bot":
        await call.answer()
        msg = await call.message.answer("Введите сообщение")
        await state.set_state("admin_send_message_as_bot")

        async with state.proxy() as data:
            data["callback_data"] = callback_data
        await asyncio.sleep(time_sleep)
        await msg.delete()

    # change settings client
    elif value == "chg_set_clt":
        await start_admin_change_settings_client(call, callback_data)

    elif value == "back_client":
        await see_card_client(call, callback_data)

    elif value == "back_list_clients":
        await search_all_clients(call, callback_data)


async def admin_send_message_as_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        callback_data = data["callback_data"]
        client_id = int(callback_data.get("user_id"))
        try:
            await bot.send_message(chat_id=client_id, text=message.text)
        except ChatNotFound:
            pass
        await state.finish()
        await asyncio.sleep(time_sleep)
        await message.delete()


async def admin_write_message_all_clients(call: types.CallbackQuery, state: FSMContext):
    all_users = await select_all_users()
    if all_users:
        await call.answer()
        msg = await call.message.answer("Введите сообщение")
        await state.set_state("send_message_all_users")
        await asyncio.sleep(time_sleep)
        await msg.delete()
    else:
        await call.answer('Список пуст')


# 2.3.2 Рассылка всем пользователям.
async def admin_send_message_all_clients(message: types.Message, state: FSMContext):
    all_users = await select_all_users()

    for user in all_users:
        if user.user_id != message.from_user.id:
            try:
                await bot.send_message(chat_id=user.user_id, text=message.text)
            except ChatNotFound:
                pass

    await state.finish()
    await message.delete()


def register_admin_manage_client_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(search_all_clients, IsAdmin() | IsSuperAdmin(),
                                       all_users_callback.filter(category="all_clients"))
    dp.register_callback_query_handler(see_card_client, IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="all_clients", value="value"))
    dp.register_callback_query_handler(moderation_client, IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="all_clients"))
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(admin_send_message_as_bot, IsAdmin() | IsSuperAdmin(),
                                state="admin_send_message_as_bot")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_write_message_all_clients, IsAdmin() | IsSuperAdmin(),
                                       text="send_message_all_users")
    dp.register_message_handler(admin_send_message_all_clients, IsAdmin() | IsSuperAdmin(),
                                state="send_message_all_users")
