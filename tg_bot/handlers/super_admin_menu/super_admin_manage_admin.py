from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands import manager_commands_users_db as commands
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, delete_user
from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers, update_post_manager
from tg_bot.filters import IsSuperAdmin
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.handlers.templetes_handlers.tmp_manage_manager import load_new_manager
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_manager, welcome_block_call
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback
from tg_bot.keyboards.manager.inline.manage_user import super_admin_manage_admins_kb, back_super_admin_manage_admins_kb


# start_manage_admins - обработка кнопки меню управления администраторами
async def start_manage_admins(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    kb = super_admin_manage_admins_kb
    welcome_text = "Меню управления администраторами"
    await welcome_block_call(call, kb, welcome_text)


# super_admin_add_admin - кнопка Добавить администратора
async def super_admin_add_admin(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="Введите: user_id username",
                                       reply_markup=back_super_admin_manage_admins_kb)
    await state.set_state("load_admin_info")
    async with state.proxy() as data:
        data["msg"] = msg


# super_admin_load_new_admin - сохраняем нового администратора
async def super_admin_load_new_admin(message: types.Message, state: FSMContext):
    await load_new_manager(message, state, manager_post="admin", cap_text="Меню управления администраторами",
                           keyboard=super_admin_manage_admins_kb, post_manager="администратор")


# ------------------------------------------------------------------------------------------------------------------

async def search_all_admins(call: types.CallbackQuery, callback_data: dict):
    admins = await select_post_managers("admin")
    super_admins = await select_post_managers("super_admin")
    all_admins = admins + super_admins
    await search_all(call, callback_data, lst_search_users=all_admins, manage_admin=True)


async def see_card_admin(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, func_get_caption=get_caption_manager, params=("super_admin_manage_admin",))


async def super_admin_manage_admin(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    admin_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")
    admin = await select_user(admin_id)

    admins = await select_post_managers("admin")
    super_admins = await select_post_managers("super_admin")
    all_admins = admins + super_admins

    # решил удалить admin`a
    if value == "del_mngr":
        if admin.manager_post == "admin" or (admin.manager_post == "super_admin" and len(super_admins) > 1):
            await call.answer()
            await delete_user(user_id=admin_id)
        else:
            await call.answer("Должен быть минимум 1 super_admin")
            return

    # решил сделать управляющего администратором
    elif value == "do_mngr_admin":
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
    elif value == "do_mngr_s_admin":
        if admin.manager_post == "admin":
            await call.answer()
            await update_post_manager(user_id=admin_id, manager_post="super_admin")
            await see_card_admin(call, callback_data)
        else:
            await call.answer("Пользователь уже super_admin")
        return

    # решил сделать управляющего модератором
    elif value == "make_mngr_moder":
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
    await call.answer(f"Количество администраторов на данный момент: {total_admins + total_super_admins}")


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
