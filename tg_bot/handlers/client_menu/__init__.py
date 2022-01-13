from aiogram import Dispatcher

from .registration_new_client import register_handlers_registration_new_client
from .client_who_liked_me import register_handlers_client_who_liked_me
from .client_mutual_liking import register_handlers_client_mutual_liking
from .client_people_nearby import register_handlers_client_people_nearby


def register_clients_handlers(dp: Dispatcher):
    register_handlers_registration_new_client(dp)
    register_handlers_client_who_liked_me(dp)
    register_handlers_client_mutual_liking(dp)
    register_handlers_client_people_nearby(dp)
