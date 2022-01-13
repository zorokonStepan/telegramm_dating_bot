from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback, change_user_card_callback


def get_change_settings_client_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                        ) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(text="Изменить имя выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_name"
                                                                                  )))

    keyboard.add(InlineKeyboardButton(text="Изменить возраст выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_age")))

    keyboard.add(InlineKeyboardButton(text="Изменить пол выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_gender")))

    keyboard.add(InlineKeyboardButton(text="Изменить биографию выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_biography")))

    keyboard.add(InlineKeyboardButton(text="Изменить или добавить фото выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_photo")))

    keyboard.add(InlineKeyboardButton(text="Изменить местоположение выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_loc")))

    keyboard.add(InlineKeyboardButton(text="Изменить пол для поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_sch_gender")))

    keyboard.add(InlineKeyboardButton(text="Изменить возраст для поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_sch_age")))

    keyboard.add(InlineKeyboardButton(text="Изменить местоположение для поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_sch_loc")))

    keyboard.add(InlineKeyboardButton(text="Изменить радиус поиска выбранного пользователя",
                                      callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                  photo_page=photo_page,
                                                                                  user_id=user_id,
                                                                                  value="chg_clt_sch_radius")))

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

    if user_status == "admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_admin"))

    elif user_status == "super_admins":
        keyboard.add(
            InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_super_admin"))

    return keyboard


def get_card_client_for_change_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                  user_photo: list,
                                  parameters: list) -> InlineKeyboardMarkup:
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

        if 1 < count_page_photo < 10:
            keyboard.row(
                InlineKeyboardButton(text="Удалить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="delete_photo")),
                InlineKeyboardButton(text="Загрузить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="insert_photo"))
            )
        elif count_page_photo == 1:
            keyboard.add(
                InlineKeyboardButton(text="Загрузить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="insert_photo"))
            )
        elif count_page_photo == 10:
            keyboard.add(
                InlineKeyboardButton(text="Удалить фото",
                                     callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                 photo_page=photo_page, user_id=user_id,
                                                                                 value="delete_photo")))

    if "back_settings" in parameters:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в список настроек",
                                          callback_data=change_user_card_callback.new(category=category, page=page,
                                                                                      photo_page=photo_page,
                                                                                      user_id=user_id,
                                                                                      value="chg_set_clt")))
    keyboard.add(InlineKeyboardButton(text="<<< Назад в общий список",
                                      callback_data=all_users_callback.new(category=category, page=page)))
    # ------------------------------------------------------------------------------------------------------------------
    if user_status == "admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_admin"))
    elif user_status == "super_admins":
        keyboard.add(
            InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_super_admin"))

    return keyboard


def get_change_client_photo_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                               user_photo: list,
                               ) -> InlineKeyboardMarkup:
    return get_card_client_for_change_kb(user_status, category, page, photo_page, user_id, user_photo,
                                         parameters=["change_photo", "manager", "back_settings"])
