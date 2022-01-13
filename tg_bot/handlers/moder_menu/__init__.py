from aiogram import Dispatcher

from .moderator_menu import register_handlers_moderator


def register_moderator_handlers(dp: Dispatcher):
    register_handlers_moderator(dp)
