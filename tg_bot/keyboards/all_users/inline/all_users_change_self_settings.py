from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.all_users.inline.all_users import get_card_user_kb
from tg_bot.keyboards.callback_datas.cb_datas import change_user_callback


def get_settings_user_kb(user_status: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(text="Изменить имя",
                                      callback_data=change_user_callback.new(param="name")))

    keyboard.add(InlineKeyboardButton(text="Изменить возраст",
                                      callback_data=change_user_callback.new(param="age")))

    keyboard.add(InlineKeyboardButton(text="Изменить пол",
                                      callback_data=change_user_callback.new(param="gender")))

    keyboard.add(InlineKeyboardButton(text="Изменить биографию",
                                      callback_data=change_user_callback.new(param="biography")))

    keyboard.add(InlineKeyboardButton(text="Изменить или добавить фото",
                                      callback_data=change_user_callback.new(param="photo")))

    keyboard.add(InlineKeyboardButton(text="Изменить местоположение",
                                      callback_data=change_user_callback.new(param="location")))

    keyboard.add(InlineKeyboardButton(text="Изменить пол для поиска",
                                      callback_data=change_user_callback.new(param="search_gender")))

    keyboard.add(InlineKeyboardButton(text="Изменить возраст для поиска",
                                      callback_data=change_user_callback.new(param="search_age")))

    keyboard.add(InlineKeyboardButton(text="Изменить местоположение для поиска",
                                      callback_data=change_user_callback.new(param="search_location")))

    keyboard.add(InlineKeyboardButton(text="Изменить радиус поиска",
                                      callback_data=change_user_callback.new(param="search_radius")))

    if user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в меню в роли клиента",
                                          callback_data="start_menu_as_client"))

    if user_status == "client":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню",
                                          callback_data="start_main_menu_client"))

    elif user_status == "moderator":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню",
                                          callback_data="start_main_menu_moderator"))
    elif user_status == "admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню",
                                          callback_data="start_main_menu_admin"))

    elif user_status == "super_admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню",
                                          callback_data="start_main_menu_super_admin"))

    return keyboard


def get_user_photo_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int, user_photo: list,
                      ) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=["change_photo", "back_settings"])
