from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, \
    delete_user_mutual_liking, delete_user_i_liked, delete_who_liked_me
from tg_bot.filters import IsSuperAdminOrAdminOrModerOrClient
from tg_bot.handlers.managers.manager import back_menu_as_client
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback

"""Меню в роли клиента. Страница Мои пары"""


# возвращает список тех кого отметил пользователь и тех с кем взаимная симпатия
async def get_all_liking_users(call):
    user = await select_user(call.from_user.id)

    # список id тех кого отметил пользователь
    users_who_i_liked_ids = user.users_i_liked
    # список id тех с кем взаимная симпатия
    users_mutual_liking_ids = user.mutual_liking

    # объединяем списки и удаляем повторы
    all_liking_users_ids = list(set(users_who_i_liked_ids + users_mutual_liking_ids))

    all_liking_users = []
    for liking_user_id in all_liking_users_ids:
        liking_user = await select_user(liking_user_id)
        all_liking_users.append(liking_user)

    return all_liking_users, users_mutual_liking_ids


# search_liking_users - выдает список тех кого отметил пользователь и тех с кем взаимная симпатия
async def search_liking_users(call: types.CallbackQuery, callback_data: dict):
    all_liking_users, users_mutual_liking_ids = await get_all_liking_users(call)
    await search_all(call, callback_data, lst_search_users=all_liking_users,
                     users_mutual_liking_id=users_mutual_liking_ids)


# see_card_liking_user - выдает выбранную карточку того кого отметил пользователь или того с кем взаимная симпатия
async def see_card_liking_user(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, params=("client_mutual_liking",))


# delete_card_liking_user - удалить пользователя из списка
# if value == "DeleteLike": проверка на случай добаления доп возможностей
async def delete_card_liking_user(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    like_user_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # допустим, user1 просматривал вкладку "мои пары"
    # отметил "Удалить"
    if value == "DeleteLike":
        await call.answer()
        # id user1 удаляется у user2 из mutual_liking если он там есть(проверка в delete_user_mutual_liking)
        await delete_user_mutual_liking(user_id=like_user_id, delete_user_id=call.from_user.id)
        # id user1 удаляется у user2 из users_i_liked если он там есть(проверка в delete_user_i_liked)
        await delete_user_i_liked(user_id=like_user_id, delete_user_id=call.from_user.id)
        # id user1 удаляется у user2 из who_liked_me если он там есть(проверка в delete_who_liked_me)
        await delete_who_liked_me(user_id=like_user_id, delete_user_id=call.from_user.id)

        # id user2 удаляется у user1 из mutual_liking если он там есть(проверка в delete_user_mutual_liking)
        await delete_user_mutual_liking(user_id=call.from_user.id, delete_user_id=like_user_id)
        # id user2 удаляется у user1 из users_i_liked если он там есть(проверка в delete_user_i_liked)
        await delete_user_i_liked(user_id=call.from_user.id, delete_user_id=like_user_id)
        # id user2 удаляется у user1 из who_liked_me если он там есть(проверка в delete_who_liked_me)
        await delete_who_liked_me(user_id=call.from_user.id, delete_user_id=like_user_id)

    all_liking_users, users_mutual_liking_ids = await get_all_liking_users(call)

    # проверяем, если есть кто то еще в парах или в отмеченных мной, то возвращаемся к списку
    if all_liking_users:
        await search_liking_users(call, callback_data)
    # иначе возвращаемся в главное меню или в меню в роли клиента
    else:
        await back_menu_as_client(call, state)


def register_handlers_client_mutual_liking(dp: Dispatcher):
    dp.register_callback_query_handler(search_liking_users,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       all_users_callback.filter(category="users_like"))
    dp.register_callback_query_handler(see_card_liking_user,
                                       IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="users_like", value="value"))
    dp.register_callback_query_handler(delete_card_liking_user, IsSuperAdminOrAdminOrModerOrClient(),
                                       user_card_callback.filter(category="users_like"))
