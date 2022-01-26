from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import all_users_callback


def manage_moderator_kb(params: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(text="Добавить модератора", callback_data="add_moder"))
    keyboard.add(InlineKeyboardButton(text="Посмотреть профили модераторов", callback_data=all_users_callback.new(
        category="moderators", page=1)))
    keyboard.add(InlineKeyboardButton(text="Количество модераторов", callback_data="count_moders"))
    keyboard.add(InlineKeyboardButton(text="Удалить всех модераторов", callback_data="delete_all_moders"))

    if "admin" in params:
        keyboard.add(
            InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_admin"))

    if "super_admin" in params:
        keyboard.add(
            InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_super_admin"))

    return keyboard


admin_manage_moderators_kb = manage_moderator_kb(params=("admin",))
super_admin_manage_moderators_kb = manage_moderator_kb(params=("super_admin",))

super_admin_manage_admins_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить администратора", callback_data="add_admin")],
        [InlineKeyboardButton(text="Посмотреть профили администраторов", callback_data=all_users_callback.new(
            category="admins", page=1))],
        [InlineKeyboardButton(text="Количество администраторов", callback_data="count_admins")],
        [InlineKeyboardButton(text="Удалить всех администраторов", callback_data="delete_all_admins")],
        [InlineKeyboardButton(text="<<< Вернуться в главное меню", callback_data="start_main_menu_super_admin")]

    ]
)

back_admin_super_admin_manage_moderators_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="<<< Назад в меню управления модераторами",
                              callback_data="back_manage_moderators_menu")]
    ]
)

back_super_admin_manage_admins_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="<<< Назад в меню управления администраторами",
                              callback_data="back_manage_admins_menu")]
    ]
)
