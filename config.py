from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
BOT_NAME = env.str("BOT_NAME")
BOT_ID = env.int("BOT_ID")

LOG_PATH = env.str("LOG_PATH")
LOG_NAME = env.str("LOG_NAME")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# первый админ будет создатель бота, затем он добавит модераторов и админов.
# модераторам и админам не нужно проходить регистрацию - заполнять анкету
SUPER_ADMIN_NAME = env.str("SUPER_ADMIN_NAME")
SUPER_ADMIN_ID = env.int("SUPER_ADMIN_ID")
SUPER_ADMIN_STATUS = env.str("SUPER_ADMIN_STATUS")

# количество карточек пользователей на одной странице
COUNT_USERS_CARDS_AT_PAGE = 5
# время в часах для временной блокировки пользователям
TIME_BANNED = 48
# время которое будут видны сообщения и после удалятся
time_sleep = 3
