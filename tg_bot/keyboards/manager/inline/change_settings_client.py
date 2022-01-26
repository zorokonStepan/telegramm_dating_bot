from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback, change_user_card_callback
from tg_bot.keyboards.keyboards_misc.for_keyboards import go_back_main_menu_admins


def get_change_settings_client_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                  ) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(text="Изменить имя выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_name"
                                                                                  )))

    keyboard.add(InlineKeyboardButton(text="Изменить возраст выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_age")))

    keyboard.add(InlineKeyboardButton(text="Изменить пол выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_gend")))

    keyboard.add(InlineKeyboardButton(text="Изменить биографию выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_braphy")))

    keyboard.add(InlineKeyboardButton(text="Изменить или добавить фото выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_ph")))

    keyboard.add(InlineKeyboardButton(text="Изменить местоположение выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_loc")))

    keyboard.add(InlineKeyboardButton(text="Изменить пол для поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_s_gend")))

    keyboard.add(InlineKeyboardButton(text="Изменить возраст для поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_s_age")))

    keyboard.add(InlineKeyboardButton(text="Изменить местоположение для поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_s_loc")))

    keyboard.add(InlineKeyboardButton(text="Изменить радиус поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_c_s_rad")))

    keyboard.add(InlineKeyboardButton(text="<<< Вернуться в профиль пользователя",
                                      callback_data=user_card_callback.new(category=category, page=page,
                                                                           photo_page=photo_page,
                                                                           user_id=user_id,
                                                                           value="back_client")))

    keyboard.add(InlineKeyboardButton(text="<<< Вернуться в список пользователей",
                                      callback_data=user_card_callback.new(category=category, page=page,
                                                                           photo_page=photo_page,
                                                                           user_id=user_id,
                                                                           value="back_list_clients")))

    # Вернуться в главное меню в зависимости от user_status
    text, callback_data = go_back_main_menu_admins(user_status)
    keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    return keyboard


def get_card_client_for_change_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                  user_photo: list, parameters: tuple) -> InlineKeyboardMarkup:
    count_page_photo = len(user_photo)
    has_next_page = count_page_photo > photo_page

    keyboard = InlineKeyboardMarkup(row_width=1)

    if user_photo and count_page_photo > 1:
        if photo_page == 1:
            keyboard.add(
                InlineKeyboardButton(text=f"Фото вперёд >>> {photo_page + 1}/{count_page_photo}",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page + 1,
                                                                                 user_id=user_id, value="value")))

        elif not has_next_page:
            keyboard.add(InlineKeyboardButton(text=f"{photo_page - 1}/{count_page_photo} <<< Фото назад",
                                              callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                          photo_page=photo_page - 1,
                                                                                          user_id=user_id,
                                                                                          value="value")))

        else:
            keyboard.row(
                InlineKeyboardButton(text=f"{photo_page - 1}/{count_page_photo} <<< Фото назад",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page - 1,
                                                                                 user_id=user_id, value="value")),
                InlineKeyboardButton(text=f"Фото вперёд >>> {photo_page + 1}/{count_page_photo}",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page + 1,
                                                                                 user_id=user_id, value="value"))
            )

    if "change_photo" in parameters:

        if count_page_photo <= 1:
            keyboard.add(
                InlineKeyboardButton(text="Загрузить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="insert_photo")))
        elif count_page_photo == 10:
            keyboard.add(
                InlineKeyboardButton(text="Удалить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="delete_photo")))

        elif count_page_photo > 1:
            keyboard.row(
                InlineKeyboardButton(text="Удалить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="delete_photo")),
                InlineKeyboardButton(text="Загрузить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="insert_photo")))

    if "back_settings" in parameters:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в список настроек",
                                          callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                      photo_page=photo_page,
                                                                                      user_id=user_id,
                                                                                      value="chg_set_clt")))
    keyboard.add(InlineKeyboardButton(text="<<< Назад в общий список",
                                      callback_data=all_users_callback.new(category=category, page=page)))
    # ------------------------------------------------------------------------------------------------------------------
    # Вернуться в главное меню в зависимости от user_status
    text, callback_data = go_back_main_menu_admins(user_status)
    keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    return keyboard


def get_change_client_photo_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                               user_photo: list,
                               ) -> InlineKeyboardMarkup:
    return get_card_client_for_change_kb(user_status, category, page, photo_page, user_id, user_photo,
                                         parameters=("change_photo", "back_settings"))
