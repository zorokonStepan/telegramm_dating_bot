from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.all_users.inline.all_users import get_card_user_kb
from tg_bot.keyboards.callback_datas.cb_datas import claim_callback


def get_card_user_who_liked_me_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                                  user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("like_dislikes",))


def get_card_like_user_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                          user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("delete_like",))


def get_card_selection_user_kb(user_status: str, category: str, page: int, photo_page: int, user_id: int,
                               user_photo: list) -> InlineKeyboardMarkup:
    return get_card_user_kb(user_status, category, page, photo_page, user_id, user_photo,
                            parameters=("like_dislikes", "complaint"))


def complaint_kb(category: str, page: int, send_claim_user_id: int, claim_user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(text="Оскорбительный текст в профиле пользователя",
                             callback_data=claim_callback.new(category=category, page=page,
                                                              send_claim_message="var_1",
                                                              send_claim_user_id=send_claim_user_id,
                                                              claim_user_id=claim_user_id)))
    keyboard.add(
        InlineKeyboardButton(text="Оскорбительные фото в профиле пользователя",
                             callback_data=claim_callback.new(category=category, page=page,
                                                              send_claim_message="var_2",
                                                              send_claim_user_id=send_claim_user_id,
                                                              claim_user_id=claim_user_id)))
    keyboard.add(
        InlineKeyboardButton(text="Напишите сообщение, пошлите его и нажмите на эту кнопку",
                             callback_data=claim_callback.new(category=category, page=page,
                                                              send_claim_message="sent_own_vers",
                                                              send_claim_user_id=send_claim_user_id,
                                                              claim_user_id=claim_user_id)))

    return keyboard
