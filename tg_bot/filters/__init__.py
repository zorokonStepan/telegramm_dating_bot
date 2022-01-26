from aiogram import Dispatcher

from tg_bot.filters.status import IsSuperAdmin, IsAdmin, IsModerator, IsNewClient, IsWaitClient, IsClient, \
    IsBannedClient, IsSuperAdminOrAdmin, IsSuperAdminOrAdminOrModer, IsSuperAdminOrAdminOrModerOrClient


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsSuperAdmin)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsModerator)

    dp.filters_factory.bind(IsNewClient)
    dp.filters_factory.bind(IsWaitClient)
    dp.filters_factory.bind(IsClient)
    dp.filters_factory.bind(IsBannedClient)

    dp.filters_factory.bind(IsSuperAdminOrAdmin)
    dp.filters_factory.bind(IsSuperAdminOrAdminOrModer)
    dp.filters_factory.bind(IsSuperAdminOrAdminOrModerOrClient)
