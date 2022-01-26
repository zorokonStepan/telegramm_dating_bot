from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.all_users.inline.start_menu_as_client import start_menu_as_client_kb
from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, all_claim_records_callback


def start_manager_kb(params: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    if "admin" in params:
        keyboard.add(InlineKeyboardButton(
            text="Меню управление клиентами", callback_data=all_users_callback.new(category="all_clients", page=1)))
        keyboard.add(InlineKeyboardButton(
            text="Меню управление модераторами", callback_data="start_manage_moderators_menu"))

    if "super_admin" in params:
        keyboard.add(InlineKeyboardButton(
            text="Меню управление администраторами", callback_data="start_manage_admins_menu"))

    if "moderator" in params:
        keyboard.add(
            InlineKeyboardButton(
                text="Пользователи, которые ожидают проверки",
                callback_data=all_users_callback.new(category="moder_wait_client", page=1)))

        keyboard.add(
            InlineKeyboardButton(
                text="Пользователи, на которых поступила жалоба",
                callback_data=all_claim_records_callback.new(page=1)))

    keyboard.add(InlineKeyboardButton(text="Меню в роли клиента", callback_data="start_menu_as_client"))

    if "admin" in params:
        keyboard.add(
            InlineKeyboardButton(text="Отправить сообщение всем пользователям", callback_data="send_message_all_users"))

    return keyboard


start_client_kb = start_menu_as_client_kb(params=("client",))
start_moderator_kb = start_manager_kb(params=("moderator",))
start_admin_kb = start_manager_kb(params=("moderator", "admin"))
start_super_admin_kb = start_manager_kb(params=("moderator", "admin", "super_admin"))
