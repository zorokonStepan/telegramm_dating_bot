from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback, change_user_callback


def start_menu_as_client_kb(params: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    if "client" in params:
        keyboard.add(InlineKeyboardButton(text="Я нравлюсь им", callback_data=all_users_callback.new(
            category="users_who_liked_me", page=1)))
        keyboard.add(InlineKeyboardButton(text="Мои пары", callback_data=all_users_callback.new(
            category="users_like", page=1)))
        keyboard.add(InlineKeyboardButton(text="Люди рядом", callback_data=all_users_callback.new(
            category="people_nearby", page=1)))
        keyboard.add(InlineKeyboardButton(text="Мои настройки", callback_data=change_user_callback.new(
            param="srt_ch_set")))

    text = "<<< Вернуться в главное меню"
    if "moderator" in params:
        keyboard.add(InlineKeyboardButton(text=text, callback_data="start_main_menu_moderator"))

    if "admin" in params:
        keyboard.add(InlineKeyboardButton(text=text, callback_data="start_main_menu_admin"))

    if "super_admin" in params:
        keyboard.add(InlineKeyboardButton(text=text, callback_data="start_main_menu_super_admin"))

    return keyboard


moderator_as_client_kb = start_menu_as_client_kb(params=("client", "moderator"))
admin_as_client_kb = start_menu_as_client_kb(params=("client", "admin"))
super_admin_as_client_kb = start_menu_as_client_kb(params=("client", "super_admin"))
