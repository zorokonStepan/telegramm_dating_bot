import asyncio
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from config import COUNT_USERS_CARDS_AT_PAGE
from create_bot import bot
from tg_bot.database.schemas.book_complaints_commands.commands_book_complaints_db import add_record
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, selection_users, \
    append_users_i_liked, append_user_who_liked_me
from tg_bot.filters import IsClient, IsModerator, IsSuperAdmin, IsAdmin
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_client
from tg_bot.handlers.managers.manager_misc import back_menu_as_client
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback, claim_callback
from tg_bot.keyboards.client.inline.inline_client_kb import get_card_selection_user_kb, complaint_kb
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


async def search_my_choice(call: types.CallbackQuery, callback_data: dict):
    my_users = await selection_users(call.from_user.id)

    if my_users:
        my_users = list(func_chunks_generators(my_users, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(my_users):
            page = len(my_users)

        category = str(callback_data.get("category"))
        user_status = await status_user(call)

        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=my_users, page=page, category=category)

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
        if IsClient():
            await call.answer('Список пуст')
        else:
            # для модераторов и администраторов
            await call.answer('Список пуст или у вас заполнены не все нужные поля в профиле.')


async def see_card_user_my_choice(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    caption = f"Мое имя: {user.name}, мне: {user.age}\n{user.biography}"
    user_status = await status_user(call)

    kb = get_card_selection_user_kb(user_status=user_status, user_photo=user.photo, user_id=user.user_id, page=page,
                                    photo_page=photo_page, category=category)
    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    try:
        await call.message.edit_media(media=photo, reply_markup=kb)
    except BadRequest:
        await call.message.delete()
        await call.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)


async def like_card_user_my_choice(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selection_user_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # допустим, я просматривал вкладку "люди рядом"
    # если я отметил жалобу
    if value == "Complaint":
        kb = complaint_kb(page=int(callback_data.get("page")), category=callback_data.get("category"),
                          send_claim_user_id=call.from_user.id, claim_user_id=selection_user_id)

        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, reply_markup=kb,
                               text="Выберите варианты нажав одну из кнопок ниже или отправьте свое сообщение и нажмите"
                                    "кнопку назад")
        await state.set_state("wait_claim")

    else:
        # если я отметил "Симпатия"
        if value == "Like":
            await call.answer()
            # у меня в колонку users_i_liked добавляется id кого я отметил
            await append_users_i_liked(user_id=call.from_user.id, append_user_id=selection_user_id)
            # пользователю кого я отметил добавляется в колонку who_liked_me мой id
            await append_user_who_liked_me(user_id=selection_user_id, append_user_id=call.from_user.id)
        # если я отметил "Пропуск"
        elif value == "Dislike":
            await call.answer()
            # ЧТО ТО НАДО ДЕЛАТЬ, ИЛИ НЕТ?
        else:
            await search_my_choice(call, callback_data)

        my_users = await selection_users(call.from_user.id)
        # проверяем, если есть кто то еще в списке отметевших меня, то возвращаемся к списку
        if my_users:
            await search_my_choice(call, callback_data)
        # иначе возвращаемся в главное меню или в меню в роли клиента
        else:
            user_status = await status_user(call)
            if user_status == "client":
                await start_main_menu_client(call)
            elif user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
                await back_menu_as_client(call)


async def complaint_user(call: Union[types.CallbackQuery, types.Message], state: FSMContext,
                         callback_data: dict = None):
    if type(call) == types.Message:
        async with state.proxy() as data:
            data["claim"] = call.text
        await asyncio.sleep(5)
        await call.delete()
    else:

        send_claim_message = callback_data.get('send_claim_message')
        send_claim_user_id = int(callback_data.get('send_claim_user_id'))
        claim_user_id = int(callback_data.get('claim_user_id'))

        # добавить жалобу в отдельную таблицу жалоб и информации о забаненных пользователях
        if send_claim_message == "var_1":
            claim = "Оскорбительный текст в профиле пользователя"
        elif send_claim_message == "var_2":
            claim = "скорбительные фото в профиле пользователя"
        elif send_claim_message == "sent_own_vers":
            async with state.proxy() as data:
                claim = data.get("claim")

        send_claim_user = await select_user(send_claim_user_id)
        claim_user = await select_user(claim_user_id)
        await add_record(send_claim_user_id=send_claim_user_id, send_claim_username=send_claim_user.username,
                         claim_user_id=claim_user_id, claim_username=claim_user.username, send_claim_message=claim)
        await state.finish()

        my_users = await selection_users(call.from_user.id)
        # проверяем, если есть кто то еще в списке отметевших меня, то возвращаемся к списку
        if my_users:
            await search_my_choice(call, callback_data)
        # иначе возвращаемся в главное меню или в меню в роли клиента
        else:
            user_status = await status_user(call)
            if user_status == "client":
                await start_main_menu_client(call)
            elif user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
                await back_menu_as_client(call)


def register_handlers_client_people_nearby(dp: Dispatcher):
    dp.register_callback_query_handler(search_my_choice,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       all_users_callback.filter(category="people_nearby"))
    dp.register_callback_query_handler(see_card_user_my_choice,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="people_nearby", value="value"))
    dp.register_callback_query_handler(like_card_user_my_choice,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="people_nearby"))
    dp.register_callback_query_handler(complaint_user, IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       claim_callback.filter(category="people_nearby"), state="wait_claim")
    dp.register_message_handler(complaint_user, IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                state="wait_claim")
