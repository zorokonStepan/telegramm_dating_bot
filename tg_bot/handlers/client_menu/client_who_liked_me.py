from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands.common_commands_users_db import search_who_liked, append_user_mutual_liking, \
    delete_who_liked_me, delete_user_i_liked
from tg_bot.filters import IsSuperAdminOrAdminOrModerOrClient
from tg_bot.handlers.managers.manager import back_menu_as_client
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_users
from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback

"""Меню в роли клиента. Страница Я им нравлюсь"""


# возвращает список тех кто отметил пользователя
async def search_all_users_who_liked_me(call: types.CallbackQuery, callback_data: dict):
    users_who_liked_me = await search_who_liked(call.from_user.id, "search_who_liked_me")
    await search_all(call, callback_data, lst_search_users=users_who_liked_me)


# see_card_user_who_liked_me - выдает выбранную карточку того кто отметил пользователя
async def see_card_user_who_liked_me(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, func_get_caption=get_caption_users, params=("client_who_liked_me",))


# like_user_who_liked_me - обработка действий над карточкой
async def like_user_who_liked_me(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    who_liked_me_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # допустим, user1 просматривал вкладку "я нравлюсь им"
    # если user1 отметил "Симпатия"
    if value == "Like":
        await call.answer()
        # у user1 в колонку mutual_liking добавляется id user2
        await append_user_mutual_liking(user_id=call.from_user.id, append_user_id=who_liked_me_id)
        # user2 добавляется в колонку mutual_liking id user1
        await append_user_mutual_liking(user_id=who_liked_me_id, append_user_id=call.from_user.id)
    # если user1 отметил "Пропуск"
    elif value == "Dislike":
        await call.answer()
        # у user2 из users_i_liked исчезает id user1
        await delete_user_i_liked(user_id=who_liked_me_id, delete_user_id=call.from_user.id)
    else:
        await search_all_users_who_liked_me(call, callback_data)

    # у user1 из колонки who_liked_me удаляется id user2
    await delete_who_liked_me(user_id=call.from_user.id, delete_user_id=who_liked_me_id)

    users_who_liked_me = await search_who_liked(call.from_user.id, "search_who_liked_me")
    # проверяем, если есть кто то еще в списке отметевших меня, то возвращаемся к списку
    if users_who_liked_me:
        await search_all_users_who_liked_me(call, callback_data)
    # иначе возвращаемся в главное меню или в меню в роли клиента
    else:
        await back_menu_as_client(call, state)


def register_handlers_client_who_liked_me(dp: Dispatcher):
    dp.register_callback_query_handler(search_all_users_who_liked_me,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       all_users_callback.filter(category="users_who_liked_me"))
    dp.register_callback_query_handler(see_card_user_who_liked_me,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="users_who_liked_me", value="value"))
    dp.register_callback_query_handler(like_user_who_liked_me, IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="users_who_liked_me"))
