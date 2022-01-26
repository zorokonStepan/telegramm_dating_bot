from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from config import COUNT_USERS_CARDS_AT_PAGE
from create_bot import bot
from tg_bot.database.schemas.book_complaints_commands.commands_book_complaints_db import select_claim_records, \
    select_claim_record, delete_claim_record, add_record
from tg_bot.database.schemas.users_commands.client_commands_users_db import select_state_clients
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user
from tg_bot.filters import IsSuperAdminOrAdminOrModer
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_moderator, start_main_menu_super_admin, \
    start_main_menu_admin
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.handlers.templetes_handlers.tmp_manage_client import tmp_banned_user_time_1, tmp_banned_user_all_time_1, \
    tmp_banned_user_2, tmp_moderation_wait_client_true, tmp_moderation_wait_client_false
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_for_managers
from tg_bot.keyboards.all_users.inline.claim_users import get_claim_clients_kb, get_card_claim_client_kb
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback, all_claim_records_callback, \
    claim_record_callback
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user

"""Меню модератора"""


async def go_main_menu_m_a_sa(call: types.CallbackQuery, state: FSMContext):
    user_status = await status_user(call)
    if user_status == "moderator":
        await start_main_menu_moderator(call, state)
    elif user_status == "admin":
        await start_main_menu_admin(call, state)
    elif user_status == "super_admin":
        await start_main_menu_super_admin(call, state)


# search_all_wait_clients - выводит список всех ожидающих модерации
async def search_all_wait_clients(call: types.CallbackQuery, callback_data: dict):
    wait_clients = await select_state_clients("wait_client")
    await search_all(call, callback_data, lst_search_users=wait_clients, wait_client=True)


# see_card_wait_client - показывает карточку выбранного ожидающего модерации
async def see_card_wait_client(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, func_get_caption=get_caption_for_managers, params=("moderator_menu",))


async def moderation_wait_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    wait_client_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # если все в порядке, то меняем состояние клиента на client и он сможет пользоваться ботом
    if value == "moder_true":
        await call.answer()
        await tmp_moderation_wait_client_true(wait_client_id)

    # если не все в порядке, то сообщаем об этом пользователю и удаляем его из БД
    elif value == "moder_false":
        await call.answer()
        await tmp_moderation_wait_client_false(wait_client_id)

    wait_clients = await select_state_clients("wait_client")
    # проверяем, если есть кто то еще ожидающий проверки, то возвращаемся к списку
    if wait_clients:
        await search_all_wait_clients(call, callback_data)
    else:
        await go_main_menu_m_a_sa(call, state)


# ---------------------------------------------------------------------------------------------------------------------
# search_all_claim_clients - выводит список всех на кого поступила жалоба
async def search_all_claim_clients(call: types.CallbackQuery, callback_data: dict):
    claim_records = await select_claim_records()

    if claim_records:
        claim_records = list(func_chunks_generators(claim_records, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(claim_records):
            page = len(claim_records)

        user_status = await status_user(call)

        kb = get_claim_clients_kb(user_status=user_status, lst_records=claim_records, page=page)
        text = f"Пользователи, на которых жаловались"
        try:
            await call.message.edit_text(text=text, reply_markup=kb)
        except BadRequest:
            await call.message.delete()
            await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=kb)
    else:
        # иначе возвращаемся в главное меню
        await call.answer('Список пуст')


# see_card_claim_client - показывает карточку
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
              f"На кого отправили жалобу: {user.client_state=}, {user.user_id=}, username: @{user.username}, {user.name=}, " \
              f"{user.age=},\n{user.biography}"

    user_status = await status_user(call)

    kb = get_card_claim_client_kb(user_status=user_status, page=page, photo_page=photo_page, user_photo=user.photo,
                                  claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id,
                                  parameters=("see_complaint",))
    if user.photo:
        photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

        try:
            await call.message.edit_media(media=photo, reply_markup=kb)
        except BadRequest:
            await call.message.delete()
            await call.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)
    else:
        try:
            await call.message.edit_text(text=caption, reply_markup=kb)
        except BadRequest:
            await call.message.delete()
            await call.message.answer(text=caption, reply_markup=kb)


async def action_claim_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    claim_user_id = int(callback_data.get("claim_user_id"))
    send_claim_user_id = int(callback_data.get("send_claim_user_id"))
    value = callback_data.get("value")

    manager = await select_user(call.from_user.id)
    claim_user = await select_user(claim_user_id)
    send_claim_user = await select_user(send_claim_user_id)
    # запись из книги жалоб
    claim_record = await select_claim_record(claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id)

    # ЗАБАНИТЬ
    if value == "ban_time" or value == "ban_all_time":
        # Можно забанить только пользователя в состоянии client
        # если нужно забанить на другой период(на время или навсегда), то сначала нужно разбанить
        if claim_user.client_state == "client":
            if value == "ban_time":
                # ЗАБАНИТЬ НА ВРЕМЯ
                await tmp_banned_user_time_1(call, claim_user_id)
            elif value == "ban_all_time":
                # ЗАБАНИТЬ НАВСЕГДА
                await tmp_banned_user_all_time_1(call, claim_user_id)

            await add_record(manager_user_id=call.from_user.id, manager_username=manager.username,
                             banned_user_id=claim_user_id, banned_username=claim_user.username,
                             banned_reason=claim_record.send_claim_message, send_claim_user_id=send_claim_user_id,
                             send_claim_username=send_claim_user.username)

        # Если пользователь уже забанен. Разбаньте его и забаньте снова.
        else:
            await tmp_banned_user_2(call, claim_user)

    # если все в порядке, то ничего не делаем
    elif value == "not_sub":
        await call.answer()

    # удаляем запись из книги жалоб
    await delete_claim_record(claim_user_id=claim_user_id, send_claim_user_id=send_claim_user_id)

    claim_records = await select_claim_records()
    # проверяем, если есть еще жалобы, то возвращаемся к списку
    if claim_records:
        await search_all_claim_clients(call, callback_data)

    else:
        # иначе возвращаемся в главное меню
        await go_main_menu_m_a_sa(call, state)


def register_handlers_moderator(dp: Dispatcher):
    # модерация нового клиента
    dp.register_callback_query_handler(search_all_wait_clients, IsSuperAdminOrAdminOrModer(),
                                       all_users_callback.filter(category="moder_wait_client"))
    dp.register_callback_query_handler(see_card_wait_client, IsSuperAdminOrAdminOrModer(),
                                       user_card_callback.filter(category="moder_wait_client", value="value"))
    dp.register_callback_query_handler(moderation_wait_client, IsSuperAdminOrAdminOrModer(),
                                       user_card_callback.filter(category="moder_wait_client"))
    # ------------------------------------------------------------------------------------------------------------------
    # просмотр жалоб
    dp.register_callback_query_handler(search_all_claim_clients, IsSuperAdminOrAdminOrModer(),
                                       all_claim_records_callback.filter())
    dp.register_callback_query_handler(see_card_claim_client, IsSuperAdminOrAdminOrModer(),
                                       claim_record_callback.filter(value="value"))
    dp.register_callback_query_handler(action_claim_client, IsSuperAdminOrAdminOrModer(),
                                       claim_record_callback.filter())
