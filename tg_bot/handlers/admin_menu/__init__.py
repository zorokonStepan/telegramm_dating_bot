from aiogram import Dispatcher

from .admin_change_settings_client import register_admin_change_settings_client_handlers
from .admin_manage_client import register_admin_manage_client_handlers
from .admin_manage_moderator import register_admin_manage_moderator_handlers

"""Пакет обработчиков доступный admin и super_admin"""


def register_admin_handlers(dp: Dispatcher):
    register_admin_manage_client_handlers(dp)
    register_admin_change_settings_client_handlers(dp)
    register_admin_manage_moderator_handlers(dp)
