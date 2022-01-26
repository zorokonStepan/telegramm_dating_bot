from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.all_users.inline.all_users import get_card_user_kb


def get_card_wait_client_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int, user_photo: list,
                            ) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("moderation", "wait_client"))


def admin_and_super_admin_get_card_client_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                             user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("banned", "moderation", "change_settings_client", "send_message_as_bot",
                                        "is_manager"))


def super_admin_get_card_moderator_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                      user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("delete_manager", "make_manager_admin", "make_manager_super_admin",
                                        "is_manager"))


def admin_get_card_moderator_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("delete_manager", "make_manager_admin", "is_manager"))


def super_admin_get_card_admin_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                  user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("delete_manager", "make_manager_admin", "make_manager_super_admin",
                                        "make_manager_moderator", "is_manager"))
