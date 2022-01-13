from aiogram import Dispatcher

from .start_main_menu import register_start_main_menu_handlers
from .change_settings import register_change_settings_handlers


def register_all_users_handlers(dp: Dispatcher):
    register_start_main_menu_handlers(dp)
    register_change_settings_handlers(dp)
