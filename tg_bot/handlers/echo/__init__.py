from aiogram import Dispatcher

from .echo import register_echo_hs


def register_echo_handlers(dp: Dispatcher):
    register_echo_hs(dp)
