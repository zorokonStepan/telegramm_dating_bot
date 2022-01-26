"""
go_back_main_menu вместо кода:

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

"""


def go_back_main_menu(user_status):
    text = "<<< Вернуться в главное меню"
    callback_data = None

    if user_status == "client":
        callback_data = "start_main_menu_client"
    elif user_status == "moderator":
        callback_data = "start_main_menu_moderator"

    elif user_status == "admin":
        callback_data = "start_main_menu_admin"

    elif user_status == "super_admin":
        callback_data = "start_main_menu_super_admin"

    return text, callback_data


"""
go_back_main_menu_admins вместо кода:

    if user_status == "admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню",
                                          callback_data="start_main_menu_admin"))

    elif user_status == "super_admin":
        keyboard.add(InlineKeyboardButton(text="<<< Вернуться в главное меню",
                                          callback_data="start_main_menu_super_admin"))
"""


def go_back_main_menu_admins(user_status):
    text = "<<< Вернуться в главное меню"
    callback_data = None

    if user_status == "admin":
        callback_data = "start_main_menu_admin"

    elif user_status == "super_admin":
        callback_data = "start_main_menu_super_admin"

    return text, callback_data
