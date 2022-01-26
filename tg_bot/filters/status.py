from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.database.schemas.users_commands.common_commands_users_db import select_user

'''Два варианта. Тот что понравиться оставить, а другой просто удалить'''


# var1 уход от избыточности кода за счет скорости работы из за дополнительной проверки

class IsUser(BoundFilter):
    """Извлекаем запись из БД users по id пользователя. Проверяем по полю manager_post какую должность он занимает или
    по полю client_state в каком состоянии пользователь. (Ксли нет ни первого ни второго, значит перед нами тот кого нет
    в нашей БД, значит начнется регистрация.
    На основании этого класса создаем все классы для проверки состояния клиента или должности управляющего ботом.
    Получаем соответствующие фильтры."""

    def __init__(self):
        self.post_manager = None
        self.state_client = None

    async def check(self, message: types.Message) -> bool:
        user = await select_user(message.from_user.id)
        if user:
            if user.client_state:
                return user.client_state == self.state_client
            elif user.manager_post:
                return user.manager_post == self.post_manager
        return False


class IsSuperAdmin(IsUser):
    def __init__(self):
        self.post_manager = "super_admin"
        self.state_client = None


class IsAdmin(IsUser):
    def __init__(self):
        self.post_manager = "admin"
        self.state_client = None


class IsModerator(IsUser):
    def __init__(self):
        self.post_manager = "moderator"
        self.state_client = None


class IsNewClient(IsUser):
    # состояние "new_client" устанавливается после ответа на первый вопрос анкеты пользователем
    def __init__(self):
        self.state_client = "new_client"
        self.post_manager = None


class IsWaitClient(IsUser):
    def __init__(self):
        self.state_client = "wait_client"
        self.post_manager = None


class IsClient(IsUser):
    def __init__(self):
        self.state_client = "client"
        self.post_manager = None


class IsBannedClient(IsUser):
    def __init__(self):
        self.state_client = "banned_client"
        self.post_manager = None

# var2 первоначальный

# class IsPostManager(BoundFilter):
#     '''
#     Извлекаем запись из БД users по id пользователя. Проверяем по полю manager_post какую должность он занимает.
#     На основании этого класса создаем все классы для управляющих ботом. Получаем фильтры для
#     проверки должности управляющего.
#     '''
#
#     def __init__(self):
#         self.post_manager = None
#
#     async def check(self, message: types.Message) -> bool:
#         manager = await select_user(message.from_user.id)
#         if manager:
#             return manager.manager_post == self.post_manager
#
#
# class IsSuperAdmin(IsPostManager):
#     def __init__(self): self.post_manager = "super_admin"
#
#
# class IsAdmin(IsPostManager):
#     def __init__(self): self.post_manager = "admin"
#
#
# class IsModerator(IsPostManager):
#     def __init__(self): self.post_manager = "moderator"
#
#
# class IsStateClient(BoundFilter):
#     '''
#     Извлекаем запись из БД users по id пользователя. Проверяем по полю client_state в каком состоянии пользователь.
#     На основании этого класса создаем все классы для клиентов. Получаем фильтры для проверки состояния клиента.
#     '''
#
#     def __init__(self):
#         self.state_client = None
#
#     async def check(self, message: types.Message) -> bool:
#         client = await select_user(message.from_user.id)
#         if client:
#             return client.client_state == self.state_client
#
#
# class IsNewClient(IsStateClient):
#     # состояние "new_client" устанавливается после ответа на первый вопрос анкеты пользователем
#     def __init__(self): self.state_client = "new_client"
#
#
# class IsWaitClient(IsStateClient):
#     def __init__(self): self.state_client = "wait_client"
#
#
# class IsClient(IsStateClient):
#     def __init__(self): self.state_client = "client"
#
#
# class IsBannedClient(IsStateClient):
#     def __init__(self): self.state_client = "banned_client"
