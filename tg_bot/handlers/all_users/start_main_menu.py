from datetime import datetime
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from create_bot import bot
from config import TIME_BANNED
from tg_bot.database.schemas.users_commands.client_commands_users_db import update_state_client
from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, update_user_username
from tg_bot.filters import IsSuperAdmin, IsAdmin, IsModerator, IsWaitClient, IsClient, IsBannedClient
from tg_bot.keyboards.all_users.inline.start_menu import start_super_admin_kb, start_admin_kb, start_moderator_kb, \
    start_client_kb
from tg_bot.states import Reg
from tg_bot.misc.for_time_banned import timedelta_to_h


async def is_change_username(msg: Union[types.Message, types.CallbackQuery]):
    if not msg.from_user.username:
        await msg.answer("У вас отсутствует username. Исправь это и снова введите команду /start.")
    else:
        user = await select_user(msg.from_user.id)
        if user.username != msg.from_user.username:
            await update_user_username(msg.from_user.id, msg.from_user.username)
            await msg.answer(f"username в БД и ваш username не совпадают."
                             f"\nВ базу данных внесены изменения: user.username={msg.from_user.username}.")


async def start_main_menu(msg: Union[types.Message, types.CallbackQuery], keyboard):
    await is_change_username(msg)
    if type(msg) == types.Message:
        await msg.answer(f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}",
                         reply_markup=keyboard)
    else:
        try:
            await msg.message.edit_text(text=f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}",
                                        reply_markup=keyboard)

        except BadRequest:
            await msg.message.delete()
            await bot.send_message(chat_id=msg.from_user.id,
                                   text=f"Добро пожаловать в Бот Знакомств, {msg.from_user.full_name}",
                                   reply_markup=keyboard)


async def start_main_menu_super_admin(msg: Union[types.Message, types.CallbackQuery]):
    await start_main_menu(msg, start_super_admin_kb)


async def start_main_menu_admin(msg: Union[types.Message, types.CallbackQuery]):
    await start_main_menu(msg, start_admin_kb)


async def start_main_menu_moderator(msg: Union[types.Message, types.CallbackQuery]):
    await start_main_menu(msg, start_moderator_kb)


async def start_new_client(message: types.Message):
    if not message.from_user.username:
        await message.answer("У вас отсутствует username. Добавьте username в настройках своего профиля в телеграмм."
                             "Без username вы не сможете использовать данный бот. "
                             "(Настройки -> Изменить профиль -> третья строка сверху @ Имя пользователя)."
                             "После установки username введите команду /start")
    else:
        await message.answer('Добро пожаловать в Бот Знакомств. Для начала давайте познакомимся. Данные, которые '
                             'вы будете вводить будут видны другим пользователям при просмотре вашей анкеты. '
                             'В дальнейшем вы сможете корректировать свои данные.'
                             ' Если захотите начать заводить данные сначала, то нажмите кнопку '
                             '"***Начать с начала***".', reply_markup=ReplyKeyboardRemove())
        # начало регистрации, продолжение в отдельном хэндлере
        await message.answer('Напишите как вас зовут:')
        await Reg.Name.set()


async def start_wait_moderation_client(message: types.Message):
    await message.answer("Ваша анкета проверяется")


async def start_main_menu_client(msg: Union[types.Message, types.CallbackQuery]):
    await start_main_menu(msg, start_client_kb)


async def start_banned_client(message: types.Message):
    user = await select_user(message.from_user.id)
    if user.time_banned:
        td = (datetime.now() - user.time_banned)
        hours_passed = timedelta_to_h(td)
        if hours_passed < TIME_BANNED:
            await message.answer(f"Вы забанены. Через {TIME_BANNED - hours_passed} часа(ов) ограничения будут сняты")
        else:
            await update_state_client(user_id=message.from_user.id, client_state="client")
            await start_main_menu_client(message)
    else:
        await message.answer("Вы забанены навсегда.")


def register_start_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(start_main_menu_super_admin, CommandStart(), IsSuperAdmin())
    dp.register_callback_query_handler(start_main_menu_super_admin, IsSuperAdmin(), text="start_main_menu_super_admin")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(start_main_menu_admin, CommandStart(), IsAdmin())
    dp.register_callback_query_handler(start_main_menu_admin, IsAdmin(), text="start_main_menu_admin")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(start_main_menu_moderator, CommandStart(), IsModerator())
    dp.register_callback_query_handler(start_main_menu_moderator, IsModerator(), text="start_main_menu_moderator")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(start_wait_moderation_client, CommandStart(), IsWaitClient())
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(start_main_menu_client, CommandStart(), IsClient())
    dp.register_callback_query_handler(start_main_menu_client, IsClient(), text="start_main_menu_client")
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(start_banned_client, CommandStart(), IsBannedClient())
    # ------------------------------------------------------------------------------------------------------------------
    dp.register_message_handler(start_new_client, CommandStart())
