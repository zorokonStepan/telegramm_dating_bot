from aiogram import Dispatcher

from .super_admin_manage_admin import register_super_admin_manage_admin_handlers


def register_super_admin_handlers(dp: Dispatcher):
    register_super_admin_manage_admin_handlers(dp)
