from tg_bot.database.schemas.users.users_db import UserDB


async def added_test_client():
    user_photo = ["AgACAgIAAxkBAAIVVmHXBjNLsQbm8-Y23DyI9ttgiil6AAKRuDEbt0G5SnOYIBGZt5-HAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVWGHXBjiHOCftNSdL9GB8BCYo1spyAAKSuDEbt0G5SgwY-nWBCU3UAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVWmHXBjxCDxslSGX1bkxayaVZBQpeAAKTuDEbt0G5SgABWhy4vmU9VwEAAwIAA3MAAyME",
                  "AgACAgIAAxkBAAIVXGHXBkFoJ0RKJQR2P3EvvqqobcTuAAKUuDEbt0G5SrT_6Fso7Q-fAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVXmHXBkVGC0kyTpcSzxT03o1iZZyYAAKVuDEbt0G5SvLlL4UPUr9PAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVYGHXBkmsQbGIgFpaVJSU0FDi7vAUAAKWuDEbt0G5SmDjDVP6AAHG0QEAAwIAA3MAAyME",
                  "AgACAgIAAxkBAAIVYmHXBk3mVuqO53j5RBHQdrmzTnJIAAKXuDEbt0G5Shx-vkkn30hbAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVZGHXBlCppNP1v4aJOZBbcI87htSlAAKYuDEbt0G5Sh-Ynf6rxuPcAQADAgADcwADIwQ"]

    biography = r'Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв.' \
                '«жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).' \
                'Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение,' \
                'происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт ' \
                'человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография ' \
                'представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных ' \
                'подробностей, и может включать в себя анализ личности субъекта.'

    biography = "test_biography"

    await UserDB(user_id=1, username="zzzz", client_state="client", name="ZZZZ", age=24,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=2, username="zzz", client_state="client", name="ZZZ", age=28,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=3, username="zz", client_state="client", name="ZZ", age=26,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=4, username="z", client_state="client", name="Z", age=24,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=5, username="ggggg", client_state="client", name="GGGGG", age=27,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=6, username="gggg", client_state="client", name="GGGG", age=23,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=7, username="ggg", client_state="client", name="GGG", age=21,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=8, username="gg", client_state="client", name="GG", age=26,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=9, username="g", client_state="client", name="G", age=30,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=10, username="fffff", client_state="client", name="FFFFF", age=20,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=11, username="ffff", client_state="client", name="FFFF", age=23,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=12, username="fff", client_state="client", name="FFF", age=29,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=13, username="ff", client_state="client", name="FF", age=18,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=14, username="f", client_state="client", name="F", age=21,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=15, username="eeeee", client_state="client", name="EEEEE", age=26,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=16, username="eeee", client_state="client", name="EEEE", age=27,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=17, username="eee", client_state="client", name="EEE", age=28,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=18, username="ee", client_state="client", name="EE", age=29,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=19, username="e", client_state="client", name="E", age=30,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=20, username="wwwww", client_state="client", name="WWWWW", age=34,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=21, username="wwww", client_state="client", name="WWWW", age=25,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=22, username="www", client_state="client", name="WWW", age=24,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=23, username="ww", client_state="client", name="WW", age=31,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=24, username="w", client_state="client", name="W", age=33,
                 gender="Женщина", biography=biography, latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()
