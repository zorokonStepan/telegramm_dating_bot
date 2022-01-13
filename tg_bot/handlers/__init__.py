from aiogram import Dispatcher

from .all_users import register_all_users_handlers
from .managers import register_manager_handlers
from .super_admin_menu import register_super_admin_handlers
from .admin_menu import register_admin_handlers
from .moder_menu import register_moderator_handlers
from .client_menu import register_clients_handlers
from .errors import register_errors_handlers

from .echo import register_echo_handlers


def register_all_handlers(dp: Dispatcher):
    register_all_users_handlers(dp)
    register_manager_handlers(dp)
    register_super_admin_handlers(dp)
    register_admin_handlers(dp)
    register_moderator_handlers(dp)
    register_clients_handlers(dp)
    register_errors_handlers(dp)

    register_echo_handlers(dp)
