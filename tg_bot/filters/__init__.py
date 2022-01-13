from aiogram import Dispatcher

from tg_bot.filters.status import IsSuperAdmin, IsAdmin, IsModerator, IsNewClient, IsWaitClient, IsClient, IsBannedClient


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsSuperAdmin)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsModerator)

    dp.filters_factory.bind(IsNewClient)
    dp.filters_factory.bind(IsWaitClient)
    dp.filters_factory.bind(IsClient)
    dp.filters_factory.bind(IsBannedClient)
