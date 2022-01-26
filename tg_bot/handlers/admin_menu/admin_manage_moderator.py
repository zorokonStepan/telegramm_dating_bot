from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands import manager_commands_users_db as commands
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, delete_user
from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers, update_post_manager
from tg_bot.filters import IsSuperAdminOrAdmin
from tg_bot.handlers.templetes_handlers.tmp_card_user import search_all, see_card
from tg_bot.handlers.templetes_handlers.tmp_manage_manager import load_new_manager
from tg_bot.handlers.templetes_handlers.tmp_misc import get_caption_manager, welcome_block_call
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, user_card_callback
from tg_bot.keyboards.manager.inline.manage_user import admin_manage_moderators_kb, super_admin_manage_moderators_kb, \
    back_admin_super_admin_manage_moderators_kb


# start_manage_moders - обработка кнопки меню управления модераторами
async def start_manage_moders(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = await select_user(call.from_user.id)

    if user.manager_post == "admin":
        kb = admin_manage_moderators_kb
    elif user.manager_post == "super_admin":
        kb = super_admin_manage_moderators_kb
    else:
        return

    welcome_text = "Меню управления модераторами"
    await welcome_block_call(call, kb, welcome_text)


# admin_add_moder - кнопка Добавить модератора
async def admin_add_moder(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="Введите: user_id username",
                                       reply_markup=back_admin_super_admin_manage_moderators_kb)
    await state.set_state("load_moder_info")
    async with state.proxy() as data:
        data["msg"] = msg


# admin_load_new_moder - сохраняем нового модератора
async def admin_load_new_moder(message: types.Message, state: FSMContext):
    await load_new_manager(message, state, manager_post="moderator", cap_text="Меню управления модераторами",
                           keyboard=admin_manage_moderators_kb, post_manager="модератор")


# search_all_moders - выводит список всех модераторов
# кнопка - просмотреть профили модераторов
async def search_all_moders(call: types.CallbackQuery, callback_data: dict):
    moderators = await select_post_managers("moderator")
    await search_all(call, callback_data, lst_search_users=moderators, manage_moder=True)


# see_card_moder - показывает карточку выбранного модератора
async def see_card_moder(call: types.CallbackQuery, callback_data: dict):
    await see_card(call, callback_data, func_get_caption=get_caption_manager, params=("admin_manage_moderator",))


# admin_manage_moder -обработка кнопок по изменению профиля модератора
async def admin_manage_moder(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    moder_id = int(callback_data.get("user_id"))
    value = callback_data.get("value")

    # решил удалить модератора
    if value == "del_mngr":
        await call.answer()
        await delete_user(user_id=moder_id)

    # admin может назначить модератора админом и все
    # super_admins может назначить модератора админом и супер_админом

    # решил сделать управляющего администратором
    elif value == "do_mngr_admin":
        await call.answer()
        await update_post_manager(user_id=moder_id, manager_post="admin")
    # решил сделать управляющего супер администратором
    elif value == "do_mngr_s_admin":
        await call.answer()
        await update_post_manager(user_id=moder_id, manager_post="super_admin")

    moderators = await select_post_managers("moderator")

    if moderators:
        await search_all_moders(call, callback_data)
    # иначе возвращаемся в главное меню
    else:
        await start_manage_moders(call, state)


# admin_count_moders - выводит количество модераторов
async def admin_count_moders(call: types.CallbackQuery):
    total_moders = await commands.count_post_managers(manager_post="moderator")
    await call.answer(f"Количество модераторов на данный момент: {total_moders}")


# admin_delete_all_moders - удаляет всех модераторов
async def admin_delete_all_moders(call: types.CallbackQuery):
    await commands.delete_post_managers(manager_post="moderator")
    await call.answer("Все модераторы удалены.")


def register_admin_manage_moderator_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_manage_moders, IsSuperAdminOrAdmin(),
                                       text="start_manage_moderators_menu")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_add_moder, IsSuperAdminOrAdmin(), text="add_moder")
    dp.register_message_handler(admin_load_new_moder, IsSuperAdminOrAdmin(), state="load_moder_info")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(search_all_moders, IsSuperAdminOrAdmin(),
                                       all_users_callback.filter(category="moderators"))
    dp.register_callback_query_handler(see_card_moder, IsSuperAdminOrAdmin(),
                                       user_card_callback.filter(category="moderators", value="value"))
    dp.register_callback_query_handler(admin_manage_moder, IsSuperAdminOrAdmin(),
                                       user_card_callback.filter(category="moderators"))
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_count_moders, IsSuperAdminOrAdmin(), text="count_moders")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_callback_query_handler(admin_delete_all_moders, IsSuperAdminOrAdmin(), text="delete_all_moders")
