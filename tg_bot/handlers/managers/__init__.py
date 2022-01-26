from .manager import register_handlers_manager

from aiogram import Dispatcher


def register_manager_handlers(dp: Dispatcher):
    register_handlers_manager(dp)
