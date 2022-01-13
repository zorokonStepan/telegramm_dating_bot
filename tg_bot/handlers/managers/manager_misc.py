from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from create_bot import bot
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user
from tg_bot.filters import IsSuperAdmin, IsAdmin, IsModerator
from tg_bot.keyboards.all_users.inline.start_menu_as_client import moderator_as_client_kb, admin_as_client_kb, \
    super_admin_as_client_kb
from tg_bot.keyboards.manager.inline.manage_user import super_admin_manage_admins_kb, super_admin_manage_moderators_kb, \
    admin_manage_moderators_kb


async def back_menu_as_client(call: types.CallbackQuery):
    user = await select_user(call.from_user.id)

    if user.manager_post == "moderator":
        kb = moderator_as_client_kb
    elif user.manager_post == "admin":
        kb = admin_as_client_kb
    elif user.manager_post == "super_admin":
        kb = super_admin_as_client_kb
    else:
        return

    try:
        await call.message.edit_text(text=f"!!! Добро пожаловать в Бот Знакомств, {call.from_user.full_name}",
                                     reply_markup=kb)
    except BadRequest:
        chat_id = call.from_user.id
        await call.message.delete()
        await bot.send_message(chat_id=chat_id,
                               text=f"!!!!! Добро пожаловать в Бот Знакомств, {call.from_user.full_name}",
                               reply_markup=kb)


async def back_admin_manage_moder_kb(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    user = await select_user(call.from_user.id)
    if user.manager_post == "admin":
        await call.message.answer(text="Меню управления модераторами", reply_markup=admin_manage_moderators_kb)
    elif user.manager_post == "super_admin":
        await call.message.answer(text="Меню управления модераторами", reply_markup=super_admin_manage_moderators_kb)


async def back_super_admin_manage_admin_kb(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text="Меню управления администраторами", reply_markup=super_admin_manage_admins_kb)


def register_manager_misc_handlers(dp: Dispatcher):
    # запуск меню как у клиента но с кнопкой вепнуться в главное меню модераторам
    dp.register_callback_query_handler(back_menu_as_client, IsSuperAdmin() | IsAdmin() | IsModerator(),
                                       text="start_menu_as_client")
    dp.register_callback_query_handler(back_admin_manage_moder_kb, IsAdmin() | IsSuperAdmin(),
                                       text="back_manage_moderators_menu", state="*")
    dp.register_callback_query_handler(back_admin_manage_moder_kb, IsSuperAdmin(),
                                       text="back_manage_admins_menu", state="*")
