from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.database.schemas.users_commands.client_commands_users_db import select_state_clients
from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers


class IsPostManager(BoundFilter):
    '''
    Извлекаем всех менеджеров с определенной должностью. Создаем список с их id. Проверяем есть ли в этом списке id
    проверяемого пользователя. На основании этого класса создаем все классы для управляющих ботом. Получаем фильтры для
    проверки должности управляющего.
    '''

    def __init__(self):
        self.manager_post = None

    async def check(self, message: types.Message) -> bool:
        managers = await select_post_managers(self.manager_post)
        managers_id = [manager.user_id for manager in managers]
        return message.from_user.id in managers_id


class IsSuperAdmin(IsPostManager):
    def __init__(self): self.manager_post = "super_admin"


class IsAdmin(IsPostManager):
    def __init__(self): self.manager_post = "admin"


class IsModerator(IsPostManager):
    def __init__(self): self.manager_post = "moderator"


class IsStateClient(BoundFilter):
    '''
    Извлекаем всех клиентов с определенным состоянием. Создаем список с их id. Проверяем есть ли в этом списке id
    проверяемого пользователя. На основании этого класса создаем все классы для клиентов бота. Получаем фильтры для
    проверки состояния клиента.
    '''

    def __init__(self):
        self.client_state = None

    async def check(self, message: types.Message) -> bool:
        # извлекаем всех пользователей с заданным статусом
        clients = await select_state_clients(self.client_state)
        clients_id = [client.user_id for client in clients]
        return message.from_user.id in clients_id


class IsNewClient(IsStateClient):
    def __init__(self): self.client_state = "new_client"


class IsWaitClient(IsStateClient):
    def __init__(self): self.client_state = "wait_client"


class IsClient(IsStateClient):
    def __init__(self): self.client_state = "client"


class IsBannedClient(IsStateClient):
    def __init__(self): self.client_state = "banned_client"

