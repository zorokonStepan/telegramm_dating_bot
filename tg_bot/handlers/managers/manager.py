from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user
from tg_bot.filters import IsSuperAdminOrAdminOrModer, IsSuperAdminOrAdmin, IsSuperAdmin
from tg_bot.handlers.all_users.start_main_menu import start_main_menu_client
from tg_bot.handlers.templetes_handlers.tmp_misc import welcome_cap, welcome_block_call
from tg_bot.keyboards.all_users.inline.start_menu_as_client import moderator_as_client_kb, admin_as_client_kb, \
    super_admin_as_client_kb
from tg_bot.keyboards.manager.inline.manage_user import super_admin_manage_admins_kb, super_admin_manage_moderators_kb, \
    admin_manage_moderators_kb
from tg_bot.misc.user_status import status_user


# back_menu_as_client - возврат на стартовую страницу в роли клиента
async def back_menu_as_client(call: types.CallbackQuery, state: FSMContext):
    user_status = await status_user(call)
    if user_status == "client":
        await start_main_menu_client(call, state)
    else:
        if user_status == "moderator":
            kb = moderator_as_client_kb
        elif user_status == "admin":
            kb = admin_as_client_kb
        elif user_status == "super_admin":
            kb = super_admin_as_client_kb
        else:
            return

        welcome_text = await welcome_cap(call)
        await welcome_block_call(call, kb, welcome_text)


# back_admin_manage_moder_kb - возврат на стартовую страницу меню управления модераторами
async def back_admin_manage_moder_kb(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    user = await select_user(call.from_user.id)
    text = "Меню управления модераторами"
    if user.manager_post == "admin":
        await call.message.answer(text=text, reply_markup=admin_manage_moderators_kb)
    elif user.manager_post == "super_admin":
        await call.message.answer(text=text, reply_markup=super_admin_manage_moderators_kb)


# back_super_admin_manage_admin_kb - возврат на стартовую страницу меню управления администраторами
async def back_super_admin_manage_admin_kb(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text="Меню управления администраторами", reply_markup=super_admin_manage_admins_kb)


def register_handlers_manager(dp: Dispatcher):
    # запуск меню как у клиента но с кнопкой вепнуться в главное меню модераторам
    dp.register_callback_query_handler(back_menu_as_client, IsSuperAdminOrAdminOrModer(), text="start_menu_as_client")
    dp.register_callback_query_handler(back_admin_manage_moder_kb, IsSuperAdminOrAdmin(),
                                       text="back_manage_moderators_menu", state="*")
    dp.register_callback_query_handler(back_super_admin_manage_admin_kb, IsSuperAdmin(),
                                       text="back_manage_admins_menu", state="*")
