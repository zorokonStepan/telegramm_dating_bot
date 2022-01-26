import asyncio
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound

from config import time_sleep
from create_bot import bot
from tg_bot.database.schemas.book_complaints_commands.commands_book_complaints_db import add_record
from tg_bot.database.schemas.users_commands.client_commands_users_db import select_states_clients, unbanned_client
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, select_all_users
from tg_bot.filters import IsSuperAdminOrAdmin
from tg_bot.handlers.admin_menu.admin_change_settings_client import start_admin_change_settings_client
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_admin, start_main_menu_super_admin
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.handlers.templetes_handlers.tmp_manage_client import tmp_banned_user_time_1, tmp_banned_user_all_time_1, \
    tmp_banned_user_2, tmp_moderation_wait_client_true, tmp_moderation_wait_client_false
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_for_managers
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback
from tg_bot.misc.user_status import status_user


# search_all_clients - обработка кнопки меню управления клиентами, выводит список всех КЛИЕНТОВ
async def search_all_clients(call: types.CallbackQuery, callback_data: dict):
    all_clients = await select_states_clients("wait_client", "client", "banned_client")
    await search_all(call, callback_data, lst_search_users=all_clients, wait_client=True)


# see_card_client - показывает карточку выбронного КЛИЕНТА
async def see_card_client(msg: Union[types.CallbackQuery, types.Message], callback_data: dict):
    await see_card(msg, callback_data, func_get_caption=get_caption_for_managers, params=("admin_manage_client",))


# moderation_client - обработка нажатых кнопок
async def moderation_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    client_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    manager = await select_user(call.from_user.id)
    client = await select_user(client_id)

    # ЗАБАНИТЬ
    if value == "admin_ban_time" or value == "admin_ban_all_time":
        # Можно забанить только пользователя в состоянии client
        # если нужно забанить на другой период(на время или навсегда), то сначала нужно разбанить
        if client.client_state == "client":
            if value == "admin_ban_time":
                # ЗАБАНИТЬ НА ВРЕМЯ
                await tmp_banned_user_time_1(call, client_id)
            elif value == "admin_ban_all_time":
                # ЗАБАНИТЬ НАВСЕГДА
                await tmp_banned_user_all_time_1(call, client_id)

            await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                             banned_user_id=client_id, banned_username=client.username)
            await see_card_client(call, callback_data)

        # Если пользователь уже забанен. Разбаньте его и забаньте снова.
        else:
            await tmp_banned_user_2(call, client)

    # РАЗБАНИТЬ
    elif value == "admin_unban":
        # забанить можно только banned_client
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

    # если это wait_client
    elif value == "moder_true" or value == "moder_false":
        if client.client_state == "wait_client":
            await call.answer()
            if value == "moder_true":
                # все в порядке, меняем состояние клиента на client и он сможет пользоваться ботом кнопка -
                # пропустить пользователя
                await tmp_moderation_wait_client_true(client_id)
                # чтобы сразу увидеть изменения состояния клиента
                await see_card_client(call, callback_data)

            elif value == "moder_false":
                # если не все в порядке, то сообщаем об этом пользователю и удаляем его из БД
                # кнопка - отклонить пользователя
                await tmp_moderation_wait_client_false(client_id)

                all_clients = await select_states_clients("wait_client", "client", "banned_client")
                if all_clients:
                    await search_all_clients(call, callback_data)
                else:
                    user_status = await status_user(call)
                    if user_status == "admin":
                        await start_main_menu_admin(call, state)
                    elif user_status == "super_admin":
                        await start_main_menu_super_admin(call, state)
        else:
            await call.answer("Доступно только для пользователей ожидающих модерацию")

    # кнопка послать сообщение от имени бота, выводит предложение ввести сообщение
    elif value == "send_mes_as_bot":
        await call.answer()
        msg = await call.message.answer("Введите сообщение")
        await state.set_state("admin_send_message_as_bot")

        async with state.proxy() as data:
            data["callback_data"] = callback_data
        await asyncio.sleep(time_sleep)
        await msg.delete()

    # change settings client
    # кнопка - изменить данные пользователя
    elif value == "chg_set_clt":
        await start_admin_change_settings_client(call, callback_data)

    # кнопка - вернуться в профиль пользователя в меню для изиенения настроек пользователя
    elif value == "back_client":
        await see_card_client(call, callback_data)

    # кнопка - вернуться в список пользоваьелей в карточке клиента и в меню для изиенения настроек пользователя
    elif value == "back_list_clients":
        await search_all_clients(call, callback_data)


# admin_send_message_as_bot - посылает сообщение от имени бота
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


# admin_write_message_all_clients - выводит предложение ввести сообщение для отправки сообщения всем пользователям
async def admin_write_message_all_users(call: types.CallbackQuery, state: FSMContext):
    all_users = await select_all_users()
    if all_users:
        await call.answer()
        msg = await call.message.answer("Введите сообщение")
        await state.set_state("send_message_all_users")
        await asyncio.sleep(time_sleep)
        await msg.delete()
    else:
        await call.answer('Список пуст')


# admin_send_message_all_clients Рассылка сообщения ВСЕМ пользователям.
async def admin_send_message_all_users(message: types.Message, state: FSMContext):
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
    dp.register_callback_query_handler(search_all_clients, IsSuperAdminOrAdmin(),
                                       all_users_callback.filter(category="all_clients"))
    dp.register_callback_query_handler(see_card_client, IsSuperAdminOrAdmin(),
                                       user_card_callback.filter(category="all_clients", value="value"))
    dp.register_callback_query_handler(moderation_client, IsSuperAdminOrAdmin(),
                                       user_card_callback.filter(category="all_clients"))
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(admin_send_message_as_bot, IsSuperAdminOrAdmin(),
                                state="admin_send_message_as_bot")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_write_message_all_users, IsSuperAdminOrAdmin(),
                                       text="send_message_all_users")
    dp.register_message_handler(admin_send_message_all_users, IsSuperAdminOrAdmin(), state="send_message_all_users")
