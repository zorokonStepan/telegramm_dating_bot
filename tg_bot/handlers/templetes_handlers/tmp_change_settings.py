from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user, delete_user_photo
from tg_bot.handlers.templetes_handlers.tmp_misc import sleep_bot_del_msg


async def change_photo_user(call: types.CallbackQuery, callback_data: dict, state: FSMContext, func_see_photos,
                            IsUserSt):
    client_id = int(callback_data.get("user_id"))
    photo_page = int(callback_data.get("photo_page"))
    value = callback_data.get("value")
    client = await select_user(client_id)

    if value == "delete_photo":

        if len(client.photo) > 1:
            await call.answer()
            await delete_user_photo(user_id=client_id, index_delete_photo=photo_page - 1)
            cb_data = callback_data
            # чтобы не выходить за index out of range
            if photo_page == 1:
                cb_data["photo_page"] = photo_page
            else:
                cb_data["photo_page"] = photo_page - 1

            await func_see_photos(call, cb_data)
        else:
            await call.answer("Должно быть минимум 1 фото")

    # фото добавляется в конец списка
    elif value == "insert_photo":
        if len(client.photo) < 10:
            await call.answer()
            msg = await call.message.answer("Отправьте фото.")
            await IsUserSt.Photo.set()
            async with state.proxy() as data:
                data["photo_page"] = photo_page
                data["call"] = call
                data["callback_data"] = callback_data

            await sleep_bot_del_msg(msg)
        else:
            await call.answer("Больше 10 фото быть не может")
