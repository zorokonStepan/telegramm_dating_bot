from typing import Union

from aiogram import types
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from config import COUNT_USERS_CARDS_AT_PAGE
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, select_users_mutual_liking_id
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_mutual_users, get_caption_users, welcome_cap, \
    welcome_block_call
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.all_users.inline.all_users_change_self_settings import get_user_photo_kb
from tg_bot.keyboards.client.inline.inline_client_kb import get_card_selection_user_kb, get_card_user_who_liked_me_kb, \
    get_card_like_user_kb
from tg_bot.keyboards.manager.inline.change_settings_client import get_change_client_photo_kb
from tg_bot.keyboards.manager.inline.get_card import admin_and_super_admin_get_card_client_kb, \
    admin_get_card_moderator_kb, super_admin_get_card_moderator_kb, get_card_wait_client_kb, \
    super_admin_get_card_admin_kb
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


# шаблон для создания и вывода нужного списка пользователей
async def search_all(call: types.CallbackQuery, callback_data: dict, lst_search_users: list,
                     users_mutual_liking_id=None, manage_moder=False, manage_admin=False, wait_client=False,
                     client_people_nearby=False):
    user_status = await status_user(call)

    if lst_search_users:
        # сортируем по возрасту
        lst_search_users = sorted(lst_search_users, key=lambda x: x.age)
        # делим список на подсписки
        search_users_cards = list(func_chunks_generators(lst_search_users, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(search_users_cards):
            page = len(search_users_cards)

        category = callback_data.get("category")

        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=search_users_cards, page=page,
                                       category=category, users_mutual_liking_id=users_mutual_liking_id,
                                       manage_moder=manage_moder, wait_client=wait_client, manage_admin=manage_admin)

        welcome_text = await welcome_cap(call)
        await welcome_block_call(call, kb, welcome_text)

    else:
        if user_status == "client":
            await call.answer('Список пуст')
        else:
            # для модераторов и администраторов
            if not client_people_nearby:
                await call.answer('Список пуст')
            else:
                # проверка нужна для "люди рядом", то есть варианты может и есть но искать их бот не будет если какие то
                # поля не заполнены
                user = await select_user(call.from_user.id)
                if not user.search_age or not user.search_gender or not user.search_latitude  \
                        or not user.search_longitude or not user.search_radius or not user.name or not user.gender \
                        or not user.latitude or not user.longitude:
                    await call.answer('У вас не заполнены некоторые поля в профиле.')
                else:
                    await call.answer('Список пуст')


# шаблон для вывода конкретной карточки пользователя
async def see_card(msg: Union[types.CallbackQuery, types.Message], callback_data: dict,
                   params: tuple, func_get_caption=None):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    if "client_mutual_liking" in params:
        users_mutual_liking_ids = await select_users_mutual_liking_id(msg.from_user.id)
        if user.user_id in users_mutual_liking_ids:
            # если взаимная симпатия пользователи видят username
            caption = await get_caption_mutual_users(user)
        else:
            caption = await get_caption_users(user)

    else:
        caption = await func_get_caption(user)

    user_status = await status_user(msg)

    if "client_people_nearby" in params:
        keyboard = get_card_selection_user_kb
    elif "client_who_liked_me" in params:
        keyboard = get_card_user_who_liked_me_kb
    elif "client_mutual_liking" in params:
        keyboard = get_card_like_user_kb
    elif "admin_manage_client" in params:
        keyboard = admin_and_super_admin_get_card_client_kb
    elif "admin_manage_moderator" in params:
        if user_status == "admin":
            # admin может назначить модератора админом и все
            keyboard = admin_get_card_moderator_kb
        elif user_status == "super_admin":
            # super_admins может назначить модератора админом и супер_админом
            keyboard = super_admin_get_card_moderator_kb
        else:
            keyboard = None
    elif "moderator_menu" in params:
        keyboard = get_card_wait_client_kb
    elif "super_admin_manage_admin" in params:
        keyboard = super_admin_get_card_admin_kb
    elif "change_settings" in params:
        keyboard = get_user_photo_kb
    elif "admin_change_settings_client" in params:
        keyboard = get_change_client_photo_kb
    else:
        keyboard = None

    kb = keyboard(user_status=user_status, user_photo=user.photo, user_id=user.user_id, page=page,
                  photo_page=photo_page, category=category)

    if user.photo:
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

    else:
        if type(msg) == types.CallbackQuery:
            try:
                await msg.message.edit_text(text=caption, reply_markup=kb)
            except BadRequest:
                await msg.message.delete()
                await msg.message.answer(text=caption, reply_markup=kb)
        else:
            try:
                await msg.edit_text(text=caption, reply_markup=kb)
            except BadRequest:
                await msg.delete()
                await msg.answer(text=caption, reply_markup=kb)
