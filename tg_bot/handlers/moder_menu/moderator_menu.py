from aiogram import types, Dispatcher
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest, ChatNotFound

from create_bot import bot
from config import COUNT_USERS_CARDS_AT_PAGE, TIME_BANNED
from tg_bot.database.schemas.book_complaints_commands.commands_book_complaints_db import select_claim_records, \
    select_claim_record, delete_claim_record, add_record
from tg_bot.database.schemas.users_commands.client_commands_users_db import select_state_clients, update_state_client, \
    banned_at_time_client, banned_all_time_client
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, delete_user
from tg_bot.filters import IsModerator, IsSuperAdmin, IsAdmin
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_moderator, start_main_menu_admin, \
    start_main_menu_super_admin
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.all_users.inline.claim_users import get_claim_clients_kb, get_card_claim_client_kb
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback, all_claim_records_callback, \
    claim_record_callback
from tg_bot.keyboards.manager.inline.get_card import get_card_wait_client_kb
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


async def search_all_wait_clients(call: types.CallbackQuery, callback_data: dict):
    wait_clients = await select_state_clients("wait_client")
    if wait_clients:
        wait_client_cards = list(func_chunks_generators(wait_clients, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(wait_client_cards):
            page = len(wait_client_cards)

        category = callback_data.get("category")
        user_status = await status_user(call)
        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=wait_client_cards, page=page,
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


async def see_card_wait_client(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    # id для отладки - удалить
    caption = f"{user.user_id=} Мое имя: {user.name}, мне: {user.age} username: @{user.username}.\n{user.biography}"
    user_status = await status_user(call)
    kb = get_card_wait_client_kb(user_id=user.user_id, user_photo=user.photo, page=page, user_status=user_status,
                                 photo_page=photo_page, category=category)

    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    try:
        await call.message.edit_media(media=photo, reply_markup=kb)
    except BadRequest:
        await call.message.delete()
        await call.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)


async def moderation_wait_client(call: types.CallbackQuery, callback_data: dict):
    wait_client_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # если все в порядке, то меняем состояние клиента на client и он сможет пользоваться ботом
    if value == "moderation_true":
        await call.answer()
        await update_state_client(user_id=wait_client_id, client_state="client")

        try:
            await bot.send_message(chat_id=wait_client_id,
                                   text="Ваша анкета прошла проверку. Можете пользоваться ботом")
        except ChatNotFound:
            pass

    # если не все в порядке, то сообщаем об этом пользователю и удаляем его из БД
    elif value == "moderation_false":
        await call.answer()

        try:
            await bot.send_message(chat_id=wait_client_id,
                                   text="Ваша анкета не прошла проверку. Можете заполнить ее снова")
        except ChatNotFound:
            pass

        await delete_user(user_id=wait_client_id)

    wait_clients = await select_state_clients("wait_client")
    # проверяем, если есть кто то еще ожидающий проверки, то возвращаемся к списку
    if wait_clients:
        await search_all_wait_clients(call, callback_data)
    else:
        user_status = await status_user(call)
        if user_status == "moderator":
            await start_main_menu_moderator(call)
        elif user_status == "admin":
            await start_main_menu_admin(call)
        elif user_status == "super_admin":
            await start_main_menu_super_admin(call)


# ---------------------------------------------------------------------------------------------------------------------

async def search_all_claim_clients(call: types.CallbackQuery, callback_data: dict):
    claim_records = await select_claim_records()

    if claim_records:
        claim_records = list(func_chunks_generators(claim_records, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(claim_records):
            page = len(claim_records)

        user_status = await status_user(call)

        kb = get_claim_clients_kb(user_status=user_status, lst_records=claim_records, page=page)
        try:
            await call.message.edit_text(text=f"Пользователи, на которых жаловались", reply_markup=kb)
        except BadRequest:
            chat_id = call.from_user.id
            await call.message.delete()
            await bot.send_message(chat_id=chat_id,
                                   text=f"Пользователи, на которых жаловались", reply_markup=kb)
    else:
        await call.answer('Список пуст')


async def see_card_claim_client(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    photo_page = int(callback_data.get("photo_page"))
    claim_user_id = int(callback_data.get("claim_user_id"))
    send_claim_user_id = int(callback_data.get("send_claim_user_id"))

    # запись из книги жалоб
    claim_record = await select_claim_record(claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id)
    # профиль пользователя на которого жалоба
    user = await select_user(claim_user_id)

    caption = f"Кто отправил жалобу: {send_claim_user_id=}, @{claim_record.send_claim_username}, " \
              f"Жалоба: {claim_record.send_claim_message}\n\n" \
              f"На кого отправили жалобу: {user.user_id=}, username: @{user.username}, {user.name=}, " \
              f"{user.age=},\n{user.biography}"

    user_status = await status_user(call)

    kb = get_card_claim_client_kb(user_status=user_status, page=page, photo_page=photo_page, user_photo=user.photo,
                                  claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id,
                                  parameters=["see_complaint"])

    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    try:
        await call.message.edit_media(media=photo, reply_markup=kb)
    except BadRequest:
        await call.message.delete()
        await call.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)


async def action_claim_client(call: types.CallbackQuery, callback_data: dict):
    claim_user_id = int(callback_data.get("claim_user_id"))
    send_claim_user_id = int(callback_data.get("send_claim_user_id"))
    value = callback_data.get("value")

    manager = await select_user(call.from_user.id)
    claim_user = await select_user(claim_user_id)
    send_claim_user = await select_user(send_claim_user_id)
    # запись из книги жалоб
    claim_record = await select_claim_record(claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id)

    if value == "banned_user_time":
        await call.answer()
        # ЗАБАНИТЬ НА ВРЕМЯ
        await update_state_client(user_id=claim_user_id, client_state="banned_client")
        await banned_at_time_client(user_id=claim_user_id)

        try:
            await bot.send_message(chat_id=claim_user_id, text=f"Вы забанены на {TIME_BANNED} часов")
        except ChatNotFound:
            pass

        await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                         banned_user_id=claim_user_id, banned_username=claim_user.username,
                         banned_reason=claim_record.send_claim_message, send_claim_user_id=send_claim_user_id,
                         send_claim_username=send_claim_user.username)

    elif value == "banned_user_all_time":
        await call.answer()
        await banned_all_time_client(user_id=claim_user_id)

        try:
            await bot.send_message(chat_id=claim_user_id, text="Вы забанены навсегда")
        except ChatNotFound:
            pass

        await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                         banned_user_id=claim_user_id, banned_username=claim_user.username,
                         banned_reason=claim_record.send_claim_message, send_claim_user_id=send_claim_user_id,
                         send_claim_username=send_claim_user.username)
    # если все в порядке, то ничего не делаем
    elif value == "not_substantiated":
        await call.answer()
    else:
        return
    # удаляем запись из книги жалоб
    await delete_claim_record(claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id)

    claim_records = await select_claim_records()
    # проверяем, если есть еще жалобы, то возвращаемся к списку
    if claim_records:
        await search_all_claim_clients(call, callback_data)
    # иначе возвращаемся в главное меню
    else:
        user_status = await status_user(call)
        if user_status == "moderator":
            await start_main_menu_moderator(call)
        elif user_status == "admin":
            await start_main_menu_admin(call)
        elif user_status == "super_admin":
            await start_main_menu_super_admin(call)


def register_handlers_moderator(dp: Dispatcher):
    # модерация нового клиента
    dp.register_callback_query_handler(search_all_wait_clients, IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       all_users_callback.filter(category="moder_wait_client"))
    dp.register_callback_query_handler(see_card_wait_client, IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="moder_wait_client", value="value"))
    dp.register_callback_query_handler(moderation_wait_client, IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="moder_wait_client"))
    # ------------------------------------------------------------------------------------------------------------------
    # просмотр жалоб
    dp.register_callback_query_handler(search_all_claim_clients, IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       all_claim_records_callback.filter())
    dp.register_callback_query_handler(see_card_claim_client, IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       claim_record_callback.filter(value="value"))
    dp.register_callback_query_handler(action_claim_client, IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       claim_record_callback.filter())
