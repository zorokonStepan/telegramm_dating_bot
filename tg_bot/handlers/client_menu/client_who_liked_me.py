from aiogram import types, Dispatcher
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from create_bot import bot
from config import COUNT_USERS_CARDS_AT_PAGE
from tg_bot.database.schemas.users_commands.common_commands_users_db import search_who_liked, append_user_mutual_liking, \
    delete_who_liked_me, delete_user_i_liked, select_user
from tg_bot.filters import IsClient, IsModerator, IsSuperAdmin, IsAdmin
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_client
from tg_bot.handlers.managers.manager_misc import back_menu_as_client
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback
from tg_bot.keyboards.client.inline.inline_client_kb import get_card_user_who_liked_me_kb
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


async def search_all_users_who_liked_me(call: types.CallbackQuery, callback_data: dict):
    users_who_liked_me = await search_who_liked(call.from_user.id, "search_who_liked_me")

    if users_who_liked_me:
        users_who_liked_me = list(func_chunks_generators(users_who_liked_me, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(users_who_liked_me):
            page = len(users_who_liked_me)

        category = str(callback_data.get("category"))
        user_status = await status_user(call)

        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=users_who_liked_me, page=page,
                                       category=category)

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


async def see_card_user_who_liked_me(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    # id для отладки - удалить
    caption = f"{user.user_id=} Мое имя: {user.name}, мне: {user.age}.\n{user.biography}"
    user_status = await status_user(call)
    kb = get_card_user_who_liked_me_kb(user_status=user_status, user_id=user.user_id, user_photo=user.photo, page=page,
                                       photo_page=photo_page, category=category)

    photo = InputMedia(type="photo", media=user.photo[photo_page - 1], caption=caption)

    try:
        await call.message.edit_media(media=photo, reply_markup=kb)
    except BadRequest:
        await call.message.delete()
        await call.message.answer_photo(photo=user.photo[photo_page - 1], caption=caption, reply_markup=kb)


async def like_user_who_liked_me(call: types.CallbackQuery, callback_data: dict):
    who_liked_me_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # допустим, я просматривал вкладку "я нравлюсь им"
    # если я отметил "Симпатия"
    if value == "Like":
        await call.answer()
        # у меня в колонку mutual_liking добавляется id того кто отметил меня первым
        await append_user_mutual_liking(user_id=call.from_user.id, append_user_id=who_liked_me_id)
        # пользователю кто отметил меня первым добавляется в колонку mutual_liking мой id
        await append_user_mutual_liking(user_id=who_liked_me_id, append_user_id=call.from_user.id)
    # если я отметил "Пропуск"
    elif value == "Dislike":
        await call.answer()
        # у того кто отметил первым из users_i_liked исчезает мое id
        await delete_user_i_liked(user_id=who_liked_me_id, delete_user_id=call.from_user.id)
    else:
        await search_all_users_who_liked_me(call, callback_data)
    # у меня из колонки who_liked_me удаляется id того кто меня отметил
    await delete_who_liked_me(user_id=call.from_user.id, delete_user_id=who_liked_me_id)

    users_who_liked_me = await search_who_liked(call.from_user.id, "search_who_liked_me")
    # проверяем, если есть кто то еще в списке отметевших меня, то возвращаемся к списку
    if users_who_liked_me:
        await search_all_users_who_liked_me(call, callback_data)
    # иначе возвращаемся в главное меню или в меню в роли клиента
    else:
        user_status = await status_user(call)
        if user_status == "client":
            await start_main_menu_client(call)
        elif user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
            await back_menu_as_client(call)


def register_handlers_client_who_liked_me(dp: Dispatcher):
    dp.register_callback_query_handler(search_all_users_who_liked_me,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       all_users_callback.filter(category="users_who_liked_me"))
    dp.register_callback_query_handler(see_card_user_who_liked_me,
                                       IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="users_who_liked_me", value="value"))
    dp.register_callback_query_handler(like_user_who_liked_me, IsClient() | IsModerator() | IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="users_who_liked_me"))
