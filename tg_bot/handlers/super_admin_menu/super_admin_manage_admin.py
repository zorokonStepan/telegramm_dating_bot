from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.utils.exceptions import BadRequest

from config import COUNT_USERS_CARDS_AT_PAGE
from create_bot import bot
from tg_bot.database.schemas.users_commands import manager_commands_users_db as commands
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_all_users, select_user, delete_user
from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers, update_post_manager
from tg_bot.filters import IsSuperAdmin
from tg_bot.keyboards.all_users.inline.all_users import get_all_selected_users_kb
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback
from tg_bot.keyboards.manager.inline.get_card import super_admin_get_card_admin_kb
from tg_bot.keyboards.manager.inline.manage_user import super_admin_manage_admins_kb, back_super_admin_manage_admins_kb
from tg_bot.misc.for_handlers import sleep_del_msg_message
from tg_bot.misc.splitting_list_parts import func_chunks_generators
from tg_bot.misc.user_status import status_user


async def start_manage_admins(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="Меню управления администраторами", reply_markup=super_admin_manage_admins_kb)


# ------------------------------------------------------------------------------------------------------------------

async def super_admin_add_admin(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="Введите: user_id username",
                                       reply_markup=back_super_admin_manage_admins_kb)
    await state.set_state("load_admin_info")
    async with state.proxy() as data:
        data["msg"] = msg


async def super_admin_load_new_admin(message: types.Message, state: FSMContext):
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
                    await commands.add_manager(username=username, user_id=user_id, manager_post="admin")

                    async with state.proxy() as data:
                        msg = data["msg"]
                        await msg.edit_text(text="Меню управления администраторами",
                                            reply_markup=super_admin_manage_admins_kb)

                    msg = await message.answer(f"Добавлен новый администратор @{username} {user_id=}")
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

async def search_all_admins(call: types.CallbackQuery, callback_data: dict):
    admins = await select_post_managers("admin")
    super_admins = await select_post_managers("super_admin")
    all_admins = admins + super_admins

    if all_admins:
        all_admins_cards = list(func_chunks_generators(all_admins, COUNT_USERS_CARDS_AT_PAGE))

        page = int(callback_data.get("page"))
        if page > len(all_admins_cards):
            page = len(all_admins_cards)

        category = callback_data.get("category")
        user_status = await status_user(call)
        kb = get_all_selected_users_kb(user_status=user_status, lst_users_cards=all_admins_cards, page=page,
                                       category=category, manage_admin=True)
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


async def see_card_admin(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    user_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    category = str(callback_data.get("category"))

    user = await select_user(user_id)

    # id для отладки - удалить
    caption = f"{user.user_id=} username: @{user.username}, {user.manager_post=}."
    user_status = await status_user(call)

    # super_admins может назначить модератора админом и супер_админом
    kb = super_admin_get_card_admin_kb(user_id=user.user_id, user_photo=user.photo, page=page,
                                       user_status=user_status, photo_page=photo_page, category=category)

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


async def super_admin_manage_admin(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    admin_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")
    admin = await select_user(admin_id)

    admins = await select_post_managers("admin")
    super_admins = await select_post_managers("super_admin")
    all_admins = admins + super_admins

    # решил удалить admin`a
    if value == "delete_manager":
        if admin.manager_post == "admin" or (admin.manager_post == "super_admin" and len(super_admins) > 1):
            await call.answer()
            await delete_user(user_id=admin_id)
        else:
            await call.answer("Должен быть минимум 1 super_admin")
            return

    # решил сделать управляющего администратором
    elif value == "make_manager_admin":
        if admin.manager_post == "admin":
            await call.answer("Пользователь уже admin")
        elif admin.manager_post == "super_admin" and len(super_admins) < 2:
            await call.answer("Должен быть минимум 1 super_admin")
        else:
            await call.answer()
            await update_post_manager(user_id=admin_id, manager_post="admin")
            await see_card_admin(call, callback_data)
        return

    # решил сделать управляющего супер администратором
    elif value == "make_manager_super_admin":
        if admin.manager_post == "admin":
            await call.answer()
            await update_post_manager(user_id=admin_id, manager_post="super_admin")
            await see_card_admin(call, callback_data)
        else:
            await call.answer("Пользователь уже super_admin")
        return

    # решил сделать управляющего модератором
    elif value == "make_manager_moderator":
        if admin.manager_post == "admin" or (admin.manager_post == "super_admin" and len(super_admins) > 1):
            await call.answer()
            await update_post_manager(user_id=admin_id, manager_post="moderator")
        else:
            await call.answer("Должен быть минимум 1 super_admin")
            return

    # всегда есть хотя бы 1 super_admin, поэтому проверки как в меню модераторов лишние
    # и блок try except в start_manage_admins отсутствует
    await search_all_admins(call, callback_data)


# ------------------------------------------------------------------------------------------------------------------
async def super_admin_count_admins(call: types.CallbackQuery):
    total_admins = await commands.count_post_managers(manager_post="admin")
    total_super_admins = await commands.count_post_managers(manager_post="super_admin")
    await call.answer(f"Количество администраторов на данный момент: {total_admins}\n"
                      f"Количество super администраторов на данный момент: {total_super_admins}\n")


async def admin_delete_all_admins(call: types.CallbackQuery):
    await commands.delete_post_managers(manager_post="admin")
    await call.answer("Все администраторы удалены.")


def register_super_admin_manage_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_manage_admins, IsSuperAdmin(), text="start_manage_admins_menu")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(super_admin_add_admin, IsSuperAdmin(), text="add_admin")
    dp.register_message_handler(super_admin_load_new_admin, IsSuperAdmin(), state="load_admin_info")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(search_all_admins, IsSuperAdmin(),
                                       all_users_callback.filter(category="admins"))
    dp.register_callback_query_handler(see_card_admin, IsSuperAdmin(),
                                       user_card_callback.filter(category="admins", value="value"))
    dp.register_callback_query_handler(super_admin_manage_admin, IsSuperAdmin(),
                                       user_card_callback.filter(category="admins"))
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(super_admin_count_admins, IsSuperAdmin(), text="count_admins")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_delete_all_admins, IsSuperAdmin(), text="delete_all_admins")
