from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user


# функция status_user для определения должности или состояния пользователя. Необходима для передачи этого параметра
# в конструкторы клавиатур и как хендлерах как фильтр.
async def status_user(msg):
    user = await select_user(msg.from_user.id)
    if user.client_state:
        user_status = user.client_state
    else:
        user_status = user.manager_post
    return user_status
