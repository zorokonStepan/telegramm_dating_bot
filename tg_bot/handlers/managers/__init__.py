from .manager_misc import register_manager_misc_handlers

from aiogram import Dispatcher


def register_manager_handlers(dp: Dispatcher):
    register_manager_misc_handlers(dp)
