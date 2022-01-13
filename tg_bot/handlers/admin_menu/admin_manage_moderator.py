from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from config import COUNT_USERS_CARDS_AT_PAGE
from create_bot import bot
from tg_bot.database.schemas.users_commands import manager_commands_users_db as commands
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_all_users, select_user, delete_user
from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers, update_post_manager
from tg_bot.filters import IsAdmin, IsSuperAdmin
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback
from tg_bot.keyboards.manager.inline.get_card import admin_get_card_moderator_kb, super_admin_get_card_moderator_kb
from tg_bot.keyboards.manager.inline.manage_user import admin_manage_moderators_kb, super_admin_manage_moderators_kb, \
    back_admin_super_admin_manage_moderators_kb
from tg_bot.misc.for_handlers import sleep_del_msg_message
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


async def start_manage_moders(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = await select_user(call.from_user.id)

    if user.manager_post == "admin":
        kb = admin_manage_moderators_kb
    elif user.manager_post == "super_admin":
        kb = super_admin_manage_moderators_kb
    else:
        return

    try:
        await call.message.edit_text(text="Меню управления модераторами", reply_markup=kb)

    except BadRequest:
        await call.message.delete()
        await call.message.answer(text="Меню управления модераторами", reply_markup=kb)


# ------------------------------------------------------------------------------------------------------------------

async def admin_add_moder(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="Введите: user_id username",
                                       reply_markup=back_admin_super_admin_manage_moderators_kb)
    await state.set_state("load_moder_info")
    async with state.proxy() as data:
        data["msg"] = msg


async def admin_load_new_moder(message: types.Message, state: FSMContext):
    user_lst = (message.text).split()
    if len(user_lst) == 2:
        if (user_lst[0]).isdigit():
            user_id = int(user_lst[0])
            username = user_lst[1].strip()
            all_users = await select_all_users()
            users_ids = [user.user_id for user in all_users]
            users_username = [user.username for user in all_users]
            if user_id not in users_ids:
                if username.startswith("@"):
                    username = username[1:]

                if username not in users_username:
                    await commands.add_manager(username=username, user_id=user_id, manager_post="moderator")

                    async with state.proxy() as data:
                        msg = data["msg"]
                        await msg.edit_text(text="Меню управления модераторами",
                                            reply_markup=admin_manage_moderators_kb)

                    msg = await message.answer(f"Добавлен новый модератор @{username} {user_id=}")
                    await state.finish()
                    await sleep_del_msg_message(msg, message)

                else:
                    msg = await message.answer("Пользователь с таким username уже есть.")
                    await sleep_del_msg_message(msg, message)
            else:
                msg = await message.answer("Пользователь с таким user_id уже есть.")
                await sleep_del_msg_message(msg, message)
        else:
            msg = await message.answer("user_id должно быть целое число.")
            await sleep_del_msg_message(msg, message)
    else:
        msg = await message.answer("Введите: user_id username.")
        await sleep_del_msg_message(msg, message)


# ------------------------------------------------------------------------------------------------------------------

async def search_all_moders(call: types.CallbackQuery, callback_data: dict):
    moderators = await select_post_managers("moderator")
    if moderators:
        moderators_cards = list(func_chunks_generators(moderators, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(moderators_cards):
            page = len(moderators_cards)

        category = callback_data.get("category")
        user_status = await status_user(call)
        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=moderators_cards, page=page,
                                       category=category, manage_moder=True)
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


async def see_card_moder(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    # id для отладки - удалить
    caption = f"{user.user_id=} username: @{user.username}, {user.manager_post=}."
    user_status = await status_user(call)

    # admin может назначить модератора админом и все
    if user_status == "admin":
        kb = admin_get_card_moderator_kb(user_id=user.user_id, user_photo=user.photo, page=page,
                                         user_status=user_status, photo_page=photo_page, category=category)
    # super_admins может назначить модератора админом и супер_админом
    elif user_status == "super_admin":
        kb = super_admin_get_card_moderator_kb(user_id=user.user_id, user_photo=user.photo, page=page,
                                               user_status=user_status, photo_page=photo_page, category=category)
    else:
        kb = None

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


async def admin_manage_moder(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    moder_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # решил удалить модератора
    if value == "delete_manager":
        await call.answer()
        await delete_user(user_id=moder_id)
    # решил сделать управляющего администратором
    elif value == "make_manager_admin":
        await call.answer()
        await update_post_manager(user_id=moder_id, manager_post="admin")
    # решил сделать управляющего супер администратором
    elif value == "make_manager_super_admin":
        await call.answer()
        await update_post_manager(user_id=moder_id, manager_post="super_admin")

    moderators = await select_post_managers("moderator")

    if moderators:
        await search_all_moders(call, callback_data)
    # иначе возвращаемся в главное меню
    else:
        await start_manage_moders(call, state)


# ------------------------------------------------------------------------------------------------------------------
async def admin_count_moders(call: types.CallbackQuery):
    total_moders = await commands.count_post_managers(manager_post="moderator")
    await call.answer(f"Количество модераторов на данный момент: {total_moders}")


async def admin_delete_all_moders(call: types.CallbackQuery):
    await commands.delete_post_managers(manager_post="moderator")
    await call.answer("Все модераторы удалены.")


def register_admin_manage_moderator_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_manage_moders, IsAdmin() | IsSuperAdmin(),
                                       text="start_manage_moderators_menu")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_add_moder, IsAdmin() | IsSuperAdmin(), text="add_moder")
    dp.register_message_handler(admin_load_new_moder, IsAdmin() | IsSuperAdmin(), state="load_moder_info")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(search_all_moders, IsAdmin() | IsSuperAdmin(),
                                       all_users_callback.filter(category="moderators"))
    dp.register_callback_query_handler(see_card_moder, IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="moderators", value="value"))
    dp.register_callback_query_handler(admin_manage_moder, IsAdmin() | IsSuperAdmin(),
                                       user_card_callback.filter(category="moderators"))
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_count_moders, IsAdmin() | IsSuperAdmin(), text="count_moders")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_delete_all_moders, IsAdmin() | IsSuperAdmin(), text="delete_all_moders")
