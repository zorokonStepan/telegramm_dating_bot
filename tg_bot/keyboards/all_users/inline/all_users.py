from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import user_card_callback, all_users_callback, change_user_callback, \
    gender_callback, change_user_card_callback
from tg_bot.keyboards.keyboards_misc.for_keyboards import go_back_main_menu


def get_name_user(users_mutual_liking_id, user):
    # лайкнутые но не просмотренные лайкнутыми пользователями карточки отмечаются *
    if users_mutual_liking_id is None:
        name = f"{user.name}"
    else:
        if user.user_id in users_mutual_liking_id:
            name = f"{user.name}"
        else:
            name = f"*{user.name}"
    return name


def get_all_selected_users_kb(user_status: str, lst_users_cards: list, page: int, category: str,
                              users_mutual_liking_id: list = None, wait_client=False,
                              manage_moder=False, manage_admin=False) -> InlineKeyboardMarkup:
    count_page = len(lst_users_cards)
    has_next_page = count_page > page

    keyboard = InlineKeyboardMarkup(row_width=1)

    for user in lst_users_cards[page - 1]:

        name = get_name_user(users_mutual_liking_id, user)

        if user_status == "moderator" or user_status == "admin" or user_status == "super_admin":

            if user.client_state:
                # если просматриваем карточку клиента
                text = f"{name}, id = {user.user_id}, возраст: {user.age}, @{user.username}, {user.client_state}"
            else:
                # если просматриваем карточку управляющего, name - может и не быть
                text = f"id = {user.user_id}, @{user.username}, {user.manager_post}"
        else:
            text = f"{name}, возрат: {user.age}"

        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=user_card_callback.new(category=category, page=page,
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

    # ------------------------------------------------------------------------------------------------------------------
    # Вернуться в главное меню в зависимости от user_status
    text, callback_data = go_back_main_menu(user_status)
    keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    return keyboard


def get_card_user_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int, user_photo: list,
                     parameters: tuple) -> InlineKeyboardMarkup:
    count_page_photo = len(user_photo)
    has_next_page = count_page_photo > photo_page

    keyboard = InlineKeyboardMarkup(row_width=1)

    # Симпатия или Пропуск
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

    # Удалить пользователя из своих пар
    if "delete_like" in parameters:
        keyboard.row(
            InlineKeyboardButton(text="Удалить пользователя из своих пар",
                                 callback_data=user_card_callback.new(category=category, page=page,
                                                                      photo_page=photo_page,
                                                                      user_id=user_id, value="DeleteLike")))

    # Послать жалобу
    if "complaint" in parameters:
        keyboard.add(InlineKeyboardButton(text="Послать жалобу",
                                          callback_data=user_card_callback.new(category=category, page=page,
                                                                               photo_page=photo_page,
                                                                               user_id=user_id, value="Complaint")))

    # у управляющих может не быть фото
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

        if count_page_photo <= 1:
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
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="moder_true")),
            InlineKeyboardButton(text="Отклонить пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="moder_false"))
        )

    if "banned" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Заблокировать пользователя на время", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="admin_ban_time")),
            InlineKeyboardButton(text="Заблокировать пользователя навсегда", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="admin_ban_all_time")),
            InlineKeyboardButton(text="Разблокировать пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="admin_unban"))
        )

    if "send_message_as_bot" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Послать сообщение от имени бота", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="send_mes_as_bot"))
        )

    if "delete_manager" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Удалить пользователя", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="del_mngr"))
        )

    if "make_manager_admin" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Сделать администратором", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id, value="do_mngr_admin")
                                 ))

    if "make_manager_super_admin" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Сделать super администратором",
                                 callback_data=user_card_callback.new(category=category, page=page,
                                                                      photo_page=photo_page, user_id=user_id,
                                                                      value="do_mngr_s_admin")
                                 ))

    if "make_manager_moderator" in parameters:
        keyboard.add(
            InlineKeyboardButton(text="Сделать модератором", callback_data=user_card_callback.new(
                category=category, page=page, photo_page=photo_page, user_id=user_id,
                value="make_mngr_moder")
                                 ))

    if "back_settings" in parameters:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в список настроек",
                                          callback_data=change_user_callback.new("srt_ch_set")))
    else:
        keyboard.add(InlineKeyboardButton(text="<<< Назад в общий список",
                                          callback_data=all_users_callback.new(category=category, page=page)))
    # ------------------------------------------------------------------------------------------------------------------

    if user_status == "moderator" or user_status == "admin" or user_status == "super_admin":
        if "wait_client" not in parameters and "is_manager" not in parameters:
            keyboard.add(InlineKeyboardButton(text="<<< Вернуться в меню в роли клиента",
                                              callback_data="start_menu_as_client"))

    # ------------------------------------------------------------------------------------------------------------------
    # Вернуться в главное меню в зависимости от user_status
    text, callback_data = go_back_main_menu(user_status)
    keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    return keyboard


def get_gender_kb(params: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    if "base" in params:
        keyboard.row(
            InlineKeyboardButton(text="Мужчина", callback_data=gender_callback.new(gender="Мужчина")),
            InlineKeyboardButton(text="Женщина", callback_data=gender_callback.new(gender="Женщина")))

    if "reg_gender_kb" in params:
        keyboard.add(InlineKeyboardButton(text="Начать с начала", callback_data="start_over"))

    return keyboard


def get_search_gender_kb(params: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    if "base" in params:
        keyboard.row(
            InlineKeyboardButton(text="Ищу мужчину", callback_data=gender_callback.new(gender="Мужчина")),
            InlineKeyboardButton(text="Ищу женщину", callback_data=gender_callback.new(gender="Женщина")))

    if "reg_search_gender_kb" in params:
        keyboard.add(InlineKeyboardButton(text="Начать с начала", callback_data="start_over"))

    return keyboard
