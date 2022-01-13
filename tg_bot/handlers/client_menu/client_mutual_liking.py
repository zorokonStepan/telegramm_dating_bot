from aiogram import types, Dispatcher
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest
from aiogram.utils.markdown import hbold

from create_bot import bot
from config import COUNT_USERS_CARDS_AT_PAGE
from tg_bot.database.schemas.users_commands.common_commands_users_db import search_who_liked, select_user, \
    select_users_mutual_liking_id, delete_user_mutual_liking, delete_user_i_liked
from tg_bot.filters import IsClient, IsModerator, IsSuperAdmin, IsAdmin
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_client
from tg_bot.handlers.managers.manager_misc import back_menu_as_client
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback
from tg_bot.keyboards.client.inline.inline_client_kb import get_card_like_user_kb
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


async def search_liking_users(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    users_who_i_liked = await search_who_liked(call.from_user.id, "search_who_i_liked")
    users_mutual_liking = await search_who_liked(call.from_user.id, "search_mutual_liking")
    users_who_i_liked_id = [user.user_id for user in users_who_i_liked]

    all_liking_users = users_who_i_liked
    # all_liking_users.extend(users_mutual_liking)
    for user in users_mutual_liking:
        if user.user_id not in users_who_i_liked_id:
            all_liking_users.append(user)

    if all_liking_users:
        # удаляем повторы из списка
        # пробовал all_liking_users = list(set(all_liking_users)) - сначала работало нормально, потом начались ошибки

        # all_liking_users = list(set(all_liking_users))

        # вариант ниже тоже выдает ошибку, не понимаю почему

        # all_liking_users_id = []
        # for user in all_liking_users:
        #     if user.user_id not in all_liking_users_id:
        #         all_liking_users_id.append(user.user_id)
        #     else:
        #         all_liking_users.remove(user)

        # сортируем по возрасту
        all_liking_users = sorted(all_liking_users, key=lambda x: x.age)
        # делим список на подсписки
        all_liking_users = list(func_chunks_generators(all_liking_users, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(all_liking_users):
            page = len(all_liking_users)

        category = str(callback_data.get("category"))

        users_mutual_liking_ids = await select_users_mutual_liking_id(call.from_user.id)

        user_status = await status_user(call)

        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=all_liking_users, page=page,
                                       category=category, users_mutual_liking_id=users_mutual_liking_ids)
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


async def see_card_liking_user(call: types.CallbackQuery, callback_data: dict):
    users_mutual_liking_ids = await select_users_mutual_liking_id(call.from_user.id)

    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    if user.user_id in users_mutual_liking_ids:
        caption = f'''Мое имя: {user.name}, мне: {user.age}, {hbold(f"связаться со мной: @{user.username}")},
        \n{user.biography}'''
    else:
        caption = f"Мое имя: {user.name}, мне: {user.age}\n{user.biography}"

    user_status = await status_user(call)

    kb = get_card_like_user_kb(user_status=user_status, category=category, page=page, photo_page=photo_page,
                               user_id=user.user_id, user_photo=user.photo)

    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    try:
        await call.message.edit_media(media=photo, reply_markup=kb)
    except BadRequest:
        await call.message.delete()
        await call.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)


async def delete_card_liking_user(call: types.CallbackQuery, callback_data: dict):
    like_user_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # допустим, я просматривал вкладку "мои пары"
    # если я отметил "Удалить"
    if value == "DeleteLike":
        await call.answer()
        # мой id удаляется у второго пользователя из mutual_liking и users_i_liked
        await delete_user_mutual_liking(user_id=like_user_id, delete_user_id=call.from_user.id)
        await delete_user_i_liked(user_id=like_user_id, delete_user_id=call.from_user.id)
        # в моих колонках удаляется id этого пользователям
        await delete_user_mutual_liking(user_id=call.from_user.id, delete_user_id=like_user_id)
        await delete_user_i_liked(user_id=call.from_user.id, delete_user_id=like_user_id)
    else:
        await search_liking_users(call, callback_data)

    users_who_i_liked = await search_who_liked(call.from_user.id, "search_who_i_liked")
    users_mutual_liking = await search_who_liked(call.from_user.id, "search_mutual_liking")
    all_liking_users = users_who_i_liked
    all_liking_users.extend(users_mutual_liking)
    # проверяем, если есть кто то еще в парах или в отмеченных мной, то возвращаемся к списку
    if all_liking_users:
        await search_liking_users(call, callback_data)
    # иначе возвращаемся в главное меню или в меню в роли клиента
    else:
        user_status = await status_user(call)
        if user_status == "client":
            await start_main_menu_client(call)
        elif user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
            await back_menu_as_client(call)


def register_handlers_client_mutual_liking(dp: Dispatcher):
    dp.register_callback_query_handler(search_liking_users,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       all_users_callback.filter(category="users_like"))
    dp.register_callback_query_handler(see_card_liking_user,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="users_like", value="value"))
    dp.register_callback_query_handler(delete_card_liking_user, IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="users_like"))
