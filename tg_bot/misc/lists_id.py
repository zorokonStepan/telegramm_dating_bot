from tg_bot.database.schemas.users_commands.manager_commands_users_db import select_post_managers


async def func_super_admins_id():
    super_admins = await select_post_managers(manager_post="super_admins")
    super_admins_id = [super_admin.user_id for super_admin in super_admins]
    return super_admins_id


async def func_admins_id():
    admins = await select_post_managers(manager_post="admin")
    admins_id = [admin.user_id for admin in admins]
    return admins_id
