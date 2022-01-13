from aiogram import Dispatcher

from .error_handler import register_errors_hs


def register_errors_handlers(dp: Dispatcher):
    register_errors_hs(dp)
