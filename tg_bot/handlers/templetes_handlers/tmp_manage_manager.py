from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.database.schemas.users_commands.common_commands_users_db import select_all_users
from tg_bot.database.schemas.users_commands.manager_commands_users_db import add_manager
from tg_bot.handlers.templetes_handlers.tmp_misc import sleep_del_msg_message


# шаблон для хендлера для добавления нового модератора или админа
async def load_new_manager(message: types.Message, state: FSMContext, manager_post: str, cap_text: str, keyboard,
                           post_manager: str):
    user_lst = (message.text).split()
    if len(user_lst) == 2:
        if (user_lst[0]).isdigit():
            user_id = int(user_lst[0])
            username = user_lst[1].strip()
            all_users = await select_all_users()
            users_ids = [user.user_id for user in all_users]
            users_username = [user.username for user in all_users]
            if user_id not in users_ids:

                if username.startswith("@"):
                    username = username[1:]

                if username not in users_username:
                    await add_manager(username=username, user_id=user_id, manager_post=manager_post)

                    async with state.proxy() as data:
                        msg = data["msg"]
                        await msg.edit_text(text=cap_text, reply_markup=keyboard)

                    msg = await message.answer(f"Добавлен новый {post_manager} @{username} {user_id=}")
                    await state.finish()
                    await sleep_del_msg_message(msg, message)

                else:
                    msg = await message.answer("Пользователь с таким username уже есть.")
                    await sleep_del_msg_message(msg, message)
            else:
                msg = await message.answer("Пользователь с таким user_id уже есть.")
                await sleep_del_msg_message(msg, message)
        else:
            msg = await message.answer("user_id должно быть целое число.")
            await sleep_del_msg_message(msg, message)
    else:
        msg = await message.answer("Введите: user_id username.")
        await sleep_del_msg_message(msg, message)
