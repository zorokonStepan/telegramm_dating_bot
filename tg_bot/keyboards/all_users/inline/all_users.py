from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback, change_user_callback, \
    change_user_card_callback, gender_callback


def get_all_selected_users_kb(user_status: str, lst_users_cards: list, page: int, category: str,
                              users_mutual_liking_id: list = None, wait_client=False,
                              manage_moder=False, manage_admin=False) -> InlineKeyboardMarkup:
    count_page = len(lst_users_cards)
    has_next_page = count_page > page

    keyboard = InlineKeyboardMarkup(row_width=1)

    for user in lst_users_cards[page - 1]:

        if user_status != "client":
            if user.client_state:
                text = f"id = {user.user_id}, @{user.username}, {user.client_state}"
            else:
                text = f"id = {user.user_id}, @{user.username}, {user.manager_post}"

        else:
            # лайкнутые но не просмотренные лайкнутыми пользователями карточки отмечаются *
            if users_mutual_liking_id is None:
                name = f"{user.name}"
            else:
                if user.user_id in users_mutual_liking_id:
                    name = f"{user.name}"
                else:
                    name = f"*{user.name}"

            text = (f"{name}, возраст: {user.age}, id = {user.user_id}")

        keyboard.add(
            InlineKeyboardButton(
                text=text, callback_data=user_card_callback.new(category=category, page=page,
                                                                photo_page=1, user_id=user.user_id,
                                                                value="value")))

    if count_page > 1:
        if page == 1:
            keyboard.add(
                InlineKeyboardButton(text=f"Вперёд >>> {page + 1}/{count_page}",
                                     callback_data=all_users_callback.new(category=category, page=(page + 1))))

        elif not has_next_page:
            keyboard.add(
                InlineKeyboardButton(text=f"{page - 1}/{count_page} <<< Назад",
                                     callback_data=all_users_callback.new(category=category, page=(page - 1))))

        else:
            keyboard.row(
                InlineKeyboardButton(text=f"{page - 1}/{count_page} <<< Назад",
                                     callback_data=all_users_callback.new(category=category, page=(page - 1))),
                InlineKeyboardButton(text=f"Вперёд >>> {page + 1}/{count_page}",
                                     callback_data=all_users_callback.new(category=category, page=(page + 1)))
            )

    if manage_moder:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в меню управления модераторами",
                                          callback_data="start_manage_moderators_menu"))
    if manage_admin:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в меню управления администраторами",
                                          callback_data="start_manage_admins_menu"))

    if user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
        if not wait_client and not manage_moder and not manage_admin:
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


def get_card_user_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int, user_photo: list,
                     parameters: list) -> InlineKeyboardMarkup:
    count_page_photo = len(user_photo)
    has_next_page = count_page_photo > photo_page

    keyboard = InlineKeyboardMarkup(row_width=1)

    if "like_dislikes" in parameters:
        keyboard.row(
            InlineKeyboardButton(text="Симпатия",
                                 callback_data=user_card_callback.new(category=category, page=page,
                                                                      photo_page=photo_page,
                                                                      user_id=user_id, value="Like")),
            InlineKeyboardButton(text="Пропуск",
                                 callback_data=user_card_callback.new(category=category, page=page,
                                                                      photo_page=photo_page,
                                                                      user_id=user_id, value="Dislike")))

    if "delete_like" in parameters:
        keyboard.row(
            InlineKeyboardButton(text="Удалить пользователя из своих пар",
                                 callback_data=user_card_callback.new(category=category, page=page,
                                                                      photo_page=photo_page,
                                                                      user_id=user_id, value="DeleteLike")))

    if "complaint" in parameters:
        keyboard.add(InlineKeyboardButton(text="Послать жалобу",
                                          callback_data=user_card_callback.new(category=category, page=page,
                                                                               photo_page=photo_page,
                                                                               user_id=user_id, value="Complaint")))

    if user_photo and count_page_photo > 1:
        if photo_page == 1:
            keyboard.add(
                InlineKeyboardButton(text=f"Фото вперёд >>> {photo_page + 1}/{count_page_photo}",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page + 1,
                                                                          user_id=user_id, value="value")))

        elif not has_next_page:
            keyboard.add(InlineKeyboardButton(text=f"{photo_page - 1}/{count_page_photo} <<< Фото назад",
                                              callback_data=user_card_callback.new(category=category, page=page,
                                                                                   photo_page=photo_page - 1,
                                                                                   user_id=user_id, value="value")))

        else:
            keyboard.row(
                InlineKeyboardButton(text=f"{photo_page - 1}/{count_page_photo} <<< Фото назад",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page - 1,
                                                                          user_id=user_id, value="value")),
                InlineKeyboardButton(text=f"Фото вперёд >>> {photo_page + 1}/{count_page_photo}",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page + 1,
                                                                          user_id=user_id, value="value"))
            )

    if "change_photo" in parameters:

        if count_page_photo == 1:
            keyboard.add(
                InlineKeyboardButton(text="Загрузить фото",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page, user_id=user_id,
                                                                          value="insert_photo"))
            )
        elif count_page_photo == 10:
            keyboard.add(
                InlineKeyboardButton(text="Удалить фото",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page, user_id=user_id,
                                                                          value="delete_photo"))
            )

        elif count_page_photo > 1:
            keyboard.row(
                InlineKeyboardButton(text="Удалить фото",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page, user_id=user_id,
                                                                          value="delete_photo")),
                InlineKeyboardButton(text="Загрузить фото",
                                     callback_data=user_card_callback.new(category=category, page=page,
                                                                          photo_page=photo_page, user_id=user_id,
                                                                          value="insert_photo"))
            )

    if "change_settings_client" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Изменить данные пользователя",
                                 callback_data=change_user_card_callback.new(category=category, page=page,
                                                                             photo_page=photo_page, user_id=user_id,
                                                                             value="chg_set_clt"))
        )

    if "moderation" in parameters:
        keyboard.row(
            InlineKeyboardButton(text="Пропустить пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="moderation_true")),
            InlineKeyboardButton(text="Отклонить пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="moderation_false"))
        )

    if "see_complaint" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Заблокировать пользователя на время", callback_data="banned_user_time"),
            InlineKeyboardButton(text="Заблокировать пользователя навсегда", callback_data="banned_user_all_time"),
            InlineKeyboardButton(text="Жалоба не обоснована", callback_data="delete_complaint")
        )

    if "banned" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Заблокировать пользователя на время", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="admin_banned_user_time")),
            InlineKeyboardButton(text="Заблокировать пользователя навсегда", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="admin_banned_user_all_time")),
            InlineKeyboardButton(text="Разблокировать пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="admin_unbanned_user"))
        )

    if "send_message_as_bot" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Послать сообщение от имени бота", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="send_message_as_bot"))
        )

    if "delete_manager" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Удалить пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="delete_manager"))
        )

    if "make_manager_admin" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Сделать администратором", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="make_manager_admin")
                                 ))

    if "make_manager_super_admin" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Сделать super администратором",
                                 callback_data=user_card_callback.new(category=category, page=page,
                                                                      photo_page=photo_page, user_id=user_id,
                                                                      value="make_manager_super_admin")
                                 ))

    if "make_manager_moderator" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Сделать модератором", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="make_manager_moderator")
                                 ))

    if "back_settings" in parameters:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в список настроек",
                                          callback_data=change_user_callback.new("start_change_settings")))
    else:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в общий список",
                                          callback_data=all_users_callback.new(category=category, page=page)))
    # ------------------------------------------------------------------------------------------------------------------

    if user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
        if "wait_client" not in parameters and "is_manager" not in parameters:
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


def get_gender_kb(params: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    if "base" in params:
        keyboard.row(
            InlineKeyboardButton(text="Мужчина", callback_data=gender_callback.new(gender="Мужчина")),
            InlineKeyboardButton(text="Женщина", callback_data=gender_callback.new(gender="Женщина")))

    if "reg_gender_kb" in params:
        keyboard.add(InlineKeyboardButton(text="Начать с начала", callback_data="start_over"))

    return keyboard


def get_search_gender_kb(params: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    if "base" in params:
        keyboard.row(
            InlineKeyboardButton(text="Ищу мужчину", callback_data=gender_callback.new(gender="Мужчина")),
            InlineKeyboardButton(text="Ищу женщину", callback_data=gender_callback.new(gender="Женщина")))

    if "reg_search_gender_kb" in params:
        keyboard.add(InlineKeyboardButton(text="Начать с начала", callback_data="start_over"))

    return keyboard
