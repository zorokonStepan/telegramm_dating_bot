from sqlalchemy import Column, BigInteger, String, sql, ARRAY, Integer, Float, DateTime

from tg_bot.database.db_gino import TimedBaseModel


class UserDB(TimedBaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, primary_key=True)
    username = Column(String(100), unique=True)

    # для клиентов new_client, wait_client, client, banned_client
    client_state = Column(String(30))
    # для управляющих super_admin, admin, moderator
    manager_post = Column(String(30))

    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    biography = Column(String(10000))
    photo = Column(ARRAY(String))
    latitude = Column(Float)
    longitude = Column(Float)

    search_gender = Column(String(20))
    search_age = Column((ARRAY(Integer)))
    search_latitude = Column(Float)
    search_longitude = Column(Float)
    search_radius = Column(Integer)

    users_i_liked = Column(ARRAY(BigInteger))
    who_liked_me = Column(ARRAY(BigInteger))
    mutual_liking = Column(ARRAY(BigInteger))

    time_banned = Column(DateTime)

    query: sql.Select
