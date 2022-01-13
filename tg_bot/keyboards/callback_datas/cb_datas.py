from aiogram.utils.callback_data import CallbackData

# --------------------для просмотра карточек пользователей--------------------------------------------------------------
all_users_callback = CallbackData("all_users_cb", "category", "page")
user_card_callback = CallbackData("user_card_cb", "category", "page", "photo_page", "user_id", "value")
claim_callback = CallbackData("claim_cb", "category", "page", "send_claim_message", "send_claim_user_id",
                              "claim_user_id")
# --------------------для настроек пользователей------------------------------------------------------------------------
gender_callback = CallbackData("gender_cb", "gender")
change_user_callback = CallbackData("change_user_cb", "param")
change_user_card_callback = CallbackData("change_user_card_cb", "category", "page", "photo_page", "user_id",
                                         "value")
# --------------------для просмотра жалоб-------------------------------------------------------------------------------
all_claim_records_callback = CallbackData("all_claim_rec_cb", "page")
claim_record_callback = CallbackData("claim_rec_cb", "page", "photo_page", "claim_user_id",
                                     "send_claim_user_id", "value")
