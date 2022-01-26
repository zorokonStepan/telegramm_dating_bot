from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user

'''Два варианта. Тот что понравиться оставить, а другой просто удалить'''


class IsUser(BoundFilter):
    """Извлекаем запись из БД users по id пользователя. Проверяем по полю manager_post какую должность он занимает или
    по полю client_state в каком состоянии пользователь. (Ксли нет ни первого ни второго, значит перед нами тот кого нет
    в нашей БД, значит начнется регистрация.
    На основании этого класса создаем все классы для проверки состояния клиента или должности управляющего ботом.
    Получаем соответствующие фильтры."""

    def __init__(self):
        self.status_user_role = None

    async def check(self, message: types.Message) -> bool:
        user = await select_user(message.from_user.id)
        if user:
            if user.client_state:
                return user.client_state in self.status_user_role
            elif user.manager_post:
                return user.manager_post in self.status_user_role
        return False


class IsSuperAdmin(IsUser):
    def __init__(self):
        self.status_user_role = ("super_admin",)


class IsAdmin(IsUser):
    def __init__(self):
        self.status_user_role = ("admin",)


class IsModerator(IsUser):
    def __init__(self):
        self.status_user_role = ("moderator",)


class IsNewClient(IsUser):
    def __init__(self):
        self.status_user_role = ("new_client",)


class IsWaitClient(IsUser):
    def __init__(self):
        self.status_user_role = ("wait_client",)


class IsClient(IsUser):
    def __init__(self):
        self.status_user_role = ("client",)


class IsBannedClient(IsUser):
    def __init__(self):
        self.status_user_role = ("banned_client",)


class IsSuperAdminOrAdmin(IsUser):
    def __init__(self):
        self.status_user_role = ("super_admin", "admin")


class IsSuperAdminOrAdminOrModer(IsUser):
    def __init__(self):
        self.status_user_role = ("super_admin", "admin", "moderator")


class IsSuperAdminOrAdminOrModerOrClient(IsUser):
    def __init__(self):
        self.status_user_role = ("super_admin", "admin", "moderator", "client")
