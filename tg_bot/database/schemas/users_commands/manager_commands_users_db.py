from asyncpg import UniqueViolationError

from tg_bot.database.schemas.users.users_db import UserDB


# добавить управляющего
# age не может быть None т.к. сортировка списков по возрасту
async def add_manager(user_id: int, username: str, manager_post: str, age=0):
    try:
        manager = UserDB(user_id=user_id, username=username, manager_post=manager_post, age=age,
                         photo=[], who_liked_me=[], users_i_liked=[], mutual_liking=[])
        await manager.create()

    except UniqueViolationError:
        pass


# список управляющих определенной должности
async def select_post_managers(manager_post: str):
    managers = await UserDB.query.where(UserDB.manager_post == manager_post).gino.all()
    return managers


# количество управляющих определенной должности
async def count_post_managers(manager_post: str):
    total = await select_post_managers(manager_post)
    return len(total)


# удалить управляющих определенной должности
async def delete_post_managers(manager_post: str):
    managers = await UserDB.query.where(UserDB.manager_post == manager_post).gino.all()
    for manager in managers:
        await manager.delete()


# изменить должность управляющего
async def update_post_manager(user_id: int, manager_post: str):
    manager = await UserDB.get(user_id)
    await manager.update(manager_post=manager_post).apply()
