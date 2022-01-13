from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_datas.cb_datas import claim_record_callback, all_claim_records_callback


def get_claim_clients_kb(user_status: str, lst_records: list, page: int) -> InlineKeyboardMarkup:
    count_page = len(lst_records)
    has_next_page = count_page > page

    keyboard = InlineKeyboardMarkup(row_width=1)

    for record in lst_records[page - 1]:
        keyboard.add(
            InlineKeyboardButton(
                text=(f"Жалоба на @{record.claim_username} от @{record.send_claim_username}"),
                callback_data=claim_record_callback.new(page=page, photo_page=1, claim_user_id=record.claim_user_id,
                                                        send_claim_user_id=record.send_claim_user_id, value="value")))

    if count_page > 1:
        if page == 1:
            keyboard.add(
                InlineKeyboardButton(text=f"Вперёд >>> {page + 1}/{count_page}",
                                     callback_data=all_claim_records_callback.new(page=(page + 1))))

        elif not has_next_page:
            keyboard.add(
                InlineKeyboardButton(text=f"{page - 1}/{count_page} <<< Назад",
                                     callback_data=all_claim_records_callback.new(page=(page - 1))))

        else:
            keyboard.row(
                InlineKeyboardButton(text=f"{page - 1}/{count_page} <<< Назад",
                                     callback_data=all_claim_records_callback.new(page=(page - 1))),
                InlineKeyboardButton(text=f"Вперёд >>> {page + 1}/{count_page}",
                                     callback_data=all_claim_records_callback.new(page=(page + 1)))
            )

    if user_status == "moderator":
        keyboard.add(
            InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start_main_menu_moderator"))

    elif user_status == "admin":
        keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start_main_menu_admin"))

    elif user_status == "super_admin":
        keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start_main_menu_super_admin"))

    return keyboard


def get_card_claim_client_kb(user_status: str, page: int, photo_page: int, user_photo: list, claim_user_id: int,
                             send_claim_user_id: int, parameters: list) -> InlineKeyboardMarkup:
    count_page_photo = len(user_photo)
    has_next_page = count_page_photo > photo_page

    keyboard = InlineKeyboardMarkup(row_width=1)

    if user_photo and count_page_photo > 1:
        if photo_page == 1:
            keyboard.add(
                InlineKeyboardButton(text=f"Фото вперёд >>> {photo_page + 1}/{count_page_photo}",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page + 1,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="value")))

        elif not has_next_page:
            keyboard.add(
                InlineKeyboardButton(text=f"{photo_page - 1}/{count_page_photo} <<< Фото назад",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page - 1,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="value")))

        else:
            keyboard.row(
                InlineKeyboardButton(text=f"{photo_page - 1}/{count_page_photo} <<< Фото назад",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page - 1,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="value")),
                InlineKeyboardButton(text=f"Фото вперёд >>> {photo_page + 1}/{count_page_photo}",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page + 1,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="value"))
            )

        if "change" in parameters:
            if 1 < count_page_photo < 10:
                keyboard.row(
                    InlineKeyboardButton(text="Удалить фото",
                                         callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                                 claim_user_id=claim_user_id,
                                                                                 send_claim_user_id=send_claim_user_id,
                                                                                 value="delete_photo")),
                    InlineKeyboardButton(text="Загрузить фото",
                                         callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                                 claim_user_id=claim_user_id,
                                                                                 send_claim_user_id=send_claim_user_id,
                                                                                 value="insert_photo"))
                )
            elif count_page_photo == 1:
                keyboard.add(
                    InlineKeyboardButton(text="Загрузить фото",
                                         callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                                 claim_user_id=claim_user_id,
                                                                                 send_claim_user_id=send_claim_user_id,
                                                                                 value="insert_photo"))
                )
            elif count_page_photo == 10:
                keyboard.add(
                    InlineKeyboardButton(text="Удалить фото",
                                         callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                                 claim_user_id=claim_user_id,
                                                                                 send_claim_user_id=send_claim_user_id,
                                                                                 value="delete_photo"))
                )

        if "see_complaint":
            keyboard.add(
                InlineKeyboardButton(text="Заблокировать пользователя на время",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="banned_user_time")))
            keyboard.add(
                InlineKeyboardButton(text="Заблокировать пользователя навсегда",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="banned_user_all_time")))
            keyboard.add(
                InlineKeyboardButton(text="Жалоба не обоснована",
                                     callback_data=claim_record_callback.new(page=page, photo_page=photo_page,
                                                                             claim_user_id=claim_user_id,
                                                                             send_claim_user_id=send_claim_user_id,
                                                                             value="not_substantiated")
                                     ))

        keyboard.add(InlineKeyboardButton(text="<<< Назад в общий список",
                                          callback_data=all_claim_records_callback.new(page=page)))

        if user_status == "moderator":
            keyboard.add(
                InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start_main_menu_moderator"))

        elif user_status == "admin":
            keyboard.add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start_main_menu_admin"))

        elif user_status == "super_admin":
            keyboard.add(
                InlineKeyboardButton(text="Вернуться в главное меню", callback_data="start_main_menu_super_admin"))

    return keyboard
