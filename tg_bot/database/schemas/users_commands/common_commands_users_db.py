from sqlalchemy import and_

from create_bot import db
from tg_bot.database.schemas.users.users_db import UserDB
from tg_bot.misc.calc_distance import calc_distance_func


async def select_user(user_id: int = None, username: str = None):
    user = None
    if user_id and username:
        user = await UserDB.query.where(
            and_(UserDB.user_id == user_id, UserDB.username == username)).gino.first()
    elif user_id and not username:
        user = await UserDB.query.where(UserDB.user_id == user_id).gino.first()
    elif username and not user_id:
        user = await UserDB.query.where(UserDB.username == username).gino.first()
    return user


async def select_all_users():
    users = await UserDB.query.gino.all()
    return users


async def count_all_users():
    total = await db.func.count(UserDB.user_id).gino.scalar()
    return total


async def delete_user(user_id: int):
    try:
        user = await UserDB.get(user_id)
        await user.delete()
        return user
    except AttributeError:
        print("*****Пользователь с таким user_id не найден*****")


async def delete_all_users():
    users = await UserDB.query.gino.all()
    for user in users:
        await user.delete()


async def update_user_username(user_id: int, username: str):
    user = await UserDB.get(user_id)
    await user.update(username=username).apply()


async def update_user_name(user_id: int, name: str):
    user = await UserDB.get(user_id)
    await user.update(name=name).apply()


async def update_user_age(user_id: int, age: int):
    user = await UserDB.get(user_id)
    await user.update(age=age).apply()


async def update_user_gender(user_id: int, gender: str):
    user = await UserDB.get(user_id)
    await user.update(gender=gender).apply()


async def update_user_biography(user_id: int, biography: str):
    user = await UserDB.get(user_id)
    await user.update(biography=biography).apply()


async def append_user_photo(user_id: int, new_photo: str):
    user = await UserDB.get(user_id)
    user.photo.append(new_photo)
    await user.update(photo=user.photo).apply()


# async def insert_user_photo(user_id: int, index_insert_photo: int, new_photo: str):
#     user = await UserDB.get(user_id)
#     user_photo = user.photo
#     user_photo.insert(index_insert_photo, new_photo)
#     await user.update(photo=user_photo).apply()


async def delete_user_photo(user_id: int, index_delete_photo: int):
    user = await UserDB.get(user_id)
    user_photo = user.photo
    user_photo.pop(index_delete_photo)
    await user.update(photo=user_photo).apply()


async def update_user_latitude(user_id: int, latitude: float):
    user = await UserDB.get(user_id)
    await user.update(latitude=latitude).apply()


async def update_user_longitude(user_id: int, longitude: float):
    user = await UserDB.get(user_id)
    await user.update(longitude=longitude).apply()


async def update_user_search_gender(user_id: int, search_gender: str):
    user = await UserDB.get(user_id)
    await user.update(search_gender=search_gender).apply()


async def update_user_search_age(user_id: int, search_age: list):
    user = await UserDB.get(user_id)
    await user.update(search_age=search_age).apply()


async def update_user_search_latitude(user_id: int, search_latitude: float):
    user = await UserDB.get(user_id)
    await user.update(search_latitude=search_latitude).apply()


async def update_user_search_longitude(user_id: int, search_longitude: float):
    user = await UserDB.get(user_id)
    await user.update(search_longitude=search_longitude).apply()


async def update_user_search_radius(user_id: int, search_radius: int):
    user = await UserDB.get(user_id)
    await user.update(search_radius=search_radius).apply()


async def search_who_liked(user_id: int, query: str):
    user = await UserDB.query.where(UserDB.user_id == user_id).gino.first()
    if query == "search_who_liked_me":
        users_ids = user.who_liked_me
    elif query == "search_who_i_liked":
        users_ids = user.users_i_liked
    elif query == "search_mutual_liking":
        users_ids = user.mutual_liking
    else:
        return
    users_profiles = []
    for user_id in users_ids:
        user = await UserDB.query.where(UserDB.user_id == user_id).gino.first()
        users_profiles.append(user)
    return users_profiles


async def selection_users(user_id: int):
    # для кого ищем
    user = await select_user(user_id)
    # проверка на наличие полей(на случай использования этих кнопок модераторами и администраторами)
    if user.search_age and user.search_gender and user.search_latitude and user.search_longitude and user.search_radius:
        # все подходящие по поиску
        sel_users = await UserDB.query.where(and_(UserDB.age >= user.search_age[0], UserDB.age <= user.search_age[1],
                                                  UserDB.gender == user.search_gender)).gino.all()

        # нам нужны только те кого нет в отмеченных или отметивших нас
        # а так же фильтруем по удаленности
        search_users = []
        # пробовал не добавлять в новый список, а удалять из sel_users - работает не корректно, не проходит весь список
        # sel_users
        all_viewed_users_id = user.users_i_liked + user.mutual_liking + user.who_liked_me
        all_viewed_users_id = list(set(all_viewed_users_id))
        for usr in sel_users:
            if usr.user_id not in all_viewed_users_id:
                if calc_distance_func(usr.latitude, usr.longitude, user.search_latitude,
                                      user.search_longitude) <= user.search_radius:
                    search_users.append(usr)

        # сортируем по удаленности
        search_users = sorted(search_users,
                              key=lambda u: calc_distance_func(u.latitude, u.longitude, user.search_latitude,
                                                               user.search_longitude))
        return search_users
    return []


async def select_users_mutual_liking_id(user_id: int):
    user = await UserDB.query.where(UserDB.user_id == user_id).gino.first()
    return user.mutual_liking


async def append_users_i_liked(user_id: int, append_user_id: int):
    user = await UserDB.get(user_id)
    users_i_liked = user.users_i_liked
    if append_user_id not in users_i_liked:
        users_i_liked.append(append_user_id)
        await user.update(users_i_liked=users_i_liked).apply()


async def append_user_who_liked_me(user_id: int, append_user_id: int):
    user = await UserDB.get(user_id)
    who_liked_me = user.who_liked_me
    if append_user_id not in who_liked_me:
        who_liked_me.append(append_user_id)
        await user.update(who_liked_me=who_liked_me).apply()


async def append_user_mutual_liking(user_id: int, append_user_id: int):
    user = await UserDB.get(user_id)
    mutual_liking = user.mutual_liking
    if append_user_id not in mutual_liking:
        mutual_liking.append(append_user_id)
        await user.update(mutual_liking=mutual_liking).apply()


async def delete_who_liked_me(user_id: int, delete_user_id: int):
    user = await UserDB.get(user_id)
    who_liked_me = user.who_liked_me
    if delete_user_id in who_liked_me:
        who_liked_me.remove(delete_user_id)
        await user.update(who_liked_me=who_liked_me).apply()


async def delete_user_i_liked(user_id: int, delete_user_id: int):
    user = await UserDB.get(user_id)
    users_i_liked = user.users_i_liked
    if delete_user_id in users_i_liked:
        users_i_liked.remove(delete_user_id)
        await user.update(users_i_liked=users_i_liked).apply()


async def delete_user_mutual_liking(user_id: int, delete_user_id: int):
    user = await UserDB.get(user_id)
    mutual_liking = user.mutual_liking
    if delete_user_id in mutual_liking:
        mutual_liking.remove(delete_user_id)
        await user.update(mutual_liking=mutual_liking).apply()
