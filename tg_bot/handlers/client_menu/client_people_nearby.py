import asyncio
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from config import time_sleep
from create_bot import bot
from tg_bot.database.schemas.book_complaints_commands.commands_book_complaints_db import add_record
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, selection_users, \
    append_users_i_liked, append_user_who_liked_me
from tg_bot.filters import IsSuperAdminOrAdminOrModerOrClient
from tg_bot.handlers.managers.manager import back_menu_as_client
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_users
from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback, claim_callback
from tg_bot.keyboards.client.inline.inline_client_kb import complaint_kb

"""Меню в роли клиента. Страница Люди рядом"""


# search_my_choice - выводит список пользователей под параметры моего запроса
async def search_my_choice(call: types.CallbackQuery, callback_data: dict):
    my_users = await selection_users(call.from_user.id)
    await search_all(call, callback_data, lst_search_users=my_users, client_people_nearby=True)


# see_card_user_my_choice - выдает выбранную карточку того кто подходит под критерии выбора
async def see_card_user_my_choice(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, func_get_caption=get_caption_users, params=("client_people_nearby",))


# like_card_user_my_choice - обработка действий над карточкой того кто подходит под критерии выбора
async def like_card_user_my_choice(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selection_user_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # допустим, user1 просматривал вкладку "люди рядом"
    # если user1 отметил кнопку послать жалобу
    if value == "Complaint":
        kb = complaint_kb(page=int(callback_data.get("page")), category=callback_data.get("category"),
                          send_claim_user_id=call.from_user.id, claim_user_id=selection_user_id)

        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, reply_markup=kb,
                               text="Выберите варианты нажав одну из кнопок ниже или отправьте свое сообщение и после "
                                    "этого нажмите кнопку назад")
        await state.set_state("wait_claim")

    else:
        # если user1 отметил "Симпатия"
        if value == "Like":
            await call.answer()
            # у user1 в колонку users_i_liked добавляется id user2
            await append_users_i_liked(user_id=call.from_user.id, append_user_id=selection_user_id)
            # пользователю user2 добавляется в колонку who_liked_me id user1
            await append_user_who_liked_me(user_id=selection_user_id, append_user_id=call.from_user.id)

        # если user1 отметил "Пропуск"
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
            await back_menu_as_client(call, state)


# complaint_user - запись жалобы
async def complaint_user(call: Union[types.CallbackQuery, types.Message], state: FSMContext,
                         callback_data: dict = None):
    if type(call) == types.Message:
        async with state.proxy() as data:
            data["claim"] = call.text
        await asyncio.sleep(time_sleep)
        await call.delete()

    else:

        send_claim_message = callback_data.get('send_claim_message')
        send_claim_user_id = int(callback_data.get('send_claim_user_id'))
        claim_user_id = int(callback_data.get('claim_user_id'))

        # добавить жалобу в отдельную таблицу жалоб и информации о забаненных пользователях
        if send_claim_message == "var_1":
            claim = "Оскорбительный текст в профиле пользователя"
        elif send_claim_message == "var_2":
            claim = "Оскорбительные фото в профиле пользователя"
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
            await back_menu_as_client(call, state)


def register_handlers_client_people_nearby(dp: Dispatcher):
    dp.register_callback_query_handler(search_my_choice,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       all_users_callback.filter(category="people_nearby"))
    dp.register_callback_query_handler(see_card_user_my_choice,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="people_nearby", value="value"))
    dp.register_callback_query_handler(like_card_user_my_choice,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="people_nearby"))
    dp.register_callback_query_handler(complaint_user, IsSuperAdminOrAdminOrModerOrClient(),
                                       claim_callback.filter(category="people_nearby"), state="wait_claim")
    dp.register_message_handler(complaint_user, IsSuperAdminOrAdminOrModerOrClient(), state="wait_claim")
