from asyncpg import UniqueViolationError
from sqlalchemy import and_, or_

from tg_bot.database.schemas.users.users_db import UserDB


async def add_manager(user_id: int, username: str, manager_post: str):
    try:
        manager = UserDB(user_id=user_id, username=username, manager_post=manager_post, photo=[], who_liked_me=[],
                         users_i_liked=[], mutual_liking=[])
        await manager.create()

    except UniqueViolationError:
        pass


async def select_post_manager(manager_post: str, user_id: int = None, username: str = None):
    manager = None
    if user_id and username:
        manager = await UserDB.query.where(
            and_(UserDB.user_id == user_id, UserDB.username == username,
                 UserDB.manager_post == manager_post)).gino.first()
    elif user_id and not username:
        manager = await UserDB.query.where(
            and_(UserDB.user_id == user_id, UserDB.manager_post == manager_post)).gino.first()
    elif username and not user_id:
        manager = await UserDB.query.where(
            and_(UserDB.username == username, UserDB.manager_post == manager_post)).gino.first()
    return manager


async def select_post_managers(manager_post: str):
    managers = await UserDB.query.where(UserDB.manager_post == manager_post).gino.all()
    return managers


async def select_one_of_two_post_manager(manager_post: tuple, user_id: int = None, username: str = None):
    manager = None
    if user_id and username:
        manager = await UserDB.query.where(
            and_(UserDB.user_id == user_id, UserDB.username == username,
                 or_(UserDB.manager_post == manager_post[0], UserDB.manager_post == manager_post[1]))).gino.first()
    elif user_id and not username:
        manager = await UserDB.query.where(and_(UserDB.user_id == user_id,
                                                or_(UserDB.manager_post == manager_post[0],
                                                    UserDB.manager_post == manager_post[1]))).gino.first()
    elif username and not user_id:
        manager = await UserDB.query.where(and_(UserDB.username == username,
                                                or_(UserDB.manager_post == manager_post[0],
                                                    UserDB.manager_post == manager_post[1]))).gino.first()
    return manager


async def select_two_post_managers(manager_post: tuple):
    managers = await UserDB.query.where(
        or_(UserDB.manager_post == manager_post[0], UserDB.manager_post == manager_post[1])).gino.all()
    return managers


async def count_post_managers(manager_post: str):
    total = await select_post_managers(manager_post)
    return len(total)


async def count_two_post_managers(manager_post: tuple):
    total = await select_two_post_managers(manager_post)
    return len(total)


async def delete_post_managers(manager_post: str):
    managers = await UserDB.query.where(UserDB.manager_post == manager_post).gino.all()
    for manager in managers:
        await manager.delete()


async def update_post_manager(user_id: int, manager_post: str):
    manager = await UserDB.get(user_id)
    await manager.update(manager_post=manager_post).apply()
