from tg_bot.database.schemas.users.users_db import UserDB


# user_photo = ["AgACAgIAAxkBAAILKmHHRRD9tsm-HZ4O1KuX5alPKHH7AAJ3uTEbMdU5Srcf_DqJGB7wAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILLGHHRRUmgGbzqsXZ1g_3mF5l4tPuAAJ1uTEbMdU5ShBQaZnXS2AoAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILLmHHRRrd1Bt6RB_-Sre_bR4-381zAAJ5uTEbMdU5Sn5Hzy8saVOCAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILMGHHRR57NBvPS5waLm8tYaNPMxbIAAJ6uTEbMdU5Spiu_9C8T35GAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILMmHHRSR71wMzU1Ef2uq8uFAfcAsMAAJ7uTEbMdU5ShyHXfFwX8wCAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILNGHHRSncdzgvtfmzBVDdLSn2fjCkAAJ8uTEbMdU5SoLLrzFzZIKWAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILNmHHRS1sas4E-ceAQ0CrgzoHk-MTAAJ9uTEbMdU5Sslgqy1SGFs8AQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILOGHHRTIE2WX4S0kqXcTE479F9BLrAAJ-uTEbMdU5SkjmQfAgmk5EAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILOmHHRTew_I5UAzcHNOygQ3xYC59PAAJ_uTEbMdU5SlMMoUCpI2roAQADAgADcwADIwQ",
#               "AgACAgIAAxkBAAILPGHHRT41Q0RWaZffsu-2_-KqwH_kAAKFuTEbMdU5SswITwEI9RH_AQADAgADcwADIwQ"]

# user_photo = ["AgACAgIAAxkBAAMUYdXiQK-VJB0X6hg-xhuwvxrSMrUAAgG3MRs7lLBKqCUMI9_smxkBAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMWYdXiRg4lqP_qr0E4aTMn1akQy44AAgK3MRs7lLBKA_tIn4mfkRcBAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMYYdXiTNZkwTJ47lkBZ7G-6HUNeVIAAgO3MRs7lLBKD_X7QMnKC40BAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMaYdXiUA9_CykhFodFL0-ugVym1OcAAgS3MRs7lLBKkh3kOV5DsmEBAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMcYdXiVWtvmjZM8bH2pWQoWGhgZe4AAgW3MRs7lLBKf4F-NBFjq4MBAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMeYdXiWQABz1x5xSthcmoB7rMSD8O3AAIGtzEbO5SwSrRCHzTU_V3rAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAMgYdXiXj7w3sqSz0WojzXceYcVnmAAAge3MRs7lLBKX-bhrAWGoFkBAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMiYdXiYhMX8j41mRYWGSexK0J3k8MAAgi3MRs7lLBKjd37jIS6OWgBAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMkYdXiZp7LupYVBrH0LTIgjmahuggAAgm3MRs7lLBKm5N2yhQCna8BAAMCAANzAAMjBA",
#                   "AgACAgIAAxkBAAMmYdXiaTBDZAPppix8A-NIt3bPUW0AAgq3MRs7lLBKAYGTQyn1BHkBAAMCAANzAAMjBA"]

# user_photo = ["AgACAgIAAxkBAAITk2HV8n1xKXSnMzcvpmALKXlY6H8-AAKMvDEblFaxSsa_5CuxWi1gAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITmWHV8n31rptr2EunIQGK7FpDMIf7AAKRvDEblFaxSnRV_SOnhYdeAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITqmHV8omQ_7UclHUabtU3n8zf1W2rAAKPvDEblFaxSsLG4VpjlYOPAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITu2HV8pECUd8E5gABye9uC9b2nQm6ewACjLwxG5RWsUrGv-QrsVotYAEAAwIAA3MAAyME",
#                   "AgACAgIAAxkBAAITvWHV8pWtZDW4V_2wZjjY0x4nk_qxAAKNvDEblFaxSpBzPpx3sIL7AQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITv2HV8pmPr_tvwQzRjS1y-oeDNqkKAAKOvDEblFaxSt-CQa1LQt82AQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITwWHV8p5-LV3Prje2LI1SJTdwQDjpAAKPvDEblFaxSsLG4VpjlYOPAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITw2HV8qLH1iun6oIr4XzTssGcL3ZyAAKQvDEblFaxSrkQr-zsgk9yAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITxWHV8qY71O63bmLyJCe6kVcSNlkIAAKSvDEblFaxSi0P18Eub0RNAQADAgADcwADIwQ",
#                   "AgACAgIAAxkBAAITx2HV8qrc-yB0ntp4DavqcVmMnn5XAAKRvDEblFaxSnRV_SOnhYdeAQADAgADcwADIwQ"]

async def added_test_client():
    user_photo = ["AgACAgIAAxkBAAIVVmHXBjNLsQbm8-Y23DyI9ttgiil6AAKRuDEbt0G5SnOYIBGZt5-HAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVWGHXBjiHOCftNSdL9GB8BCYo1spyAAKSuDEbt0G5SgwY-nWBCU3UAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVWmHXBjxCDxslSGX1bkxayaVZBQpeAAKTuDEbt0G5SgABWhy4vmU9VwEAAwIAA3MAAyME",
                  "AgACAgIAAxkBAAIVXGHXBkFoJ0RKJQR2P3EvvqqobcTuAAKUuDEbt0G5SrT_6Fso7Q-fAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVXmHXBkVGC0kyTpcSzxT03o1iZZyYAAKVuDEbt0G5SvLlL4UPUr9PAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVYGHXBkmsQbGIgFpaVJSU0FDi7vAUAAKWuDEbt0G5SmDjDVP6AAHG0QEAAwIAA3MAAyME",
                  "AgACAgIAAxkBAAIVYmHXBk3mVuqO53j5RBHQdrmzTnJIAAKXuDEbt0G5Shx-vkkn30hbAQADAgADcwADIwQ",
                  "AgACAgIAAxkBAAIVZGHXBlCppNP1v4aJOZBbcI87htSlAAKYuDEbt0G5Sh-Ynf6rxuPcAQADAgADcwADIwQ"]

    await UserDB(user_id=909928714, username="stepan_kolodkin", client_state="client", name="Stepan", age=32,
                 gender="Мужчина", biography="hhhh", latitude=59.848311, longitude=30.361708, search_gender="Женщина",
                 photo=user_photo,
                 search_age=[18, 40], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[1, 3, 5, 7, 9, 11, 13],
                 who_liked_me=[2, 4, 6, 8, 10, 12, 14], mutual_liking=[]).create()

    await UserDB(user_id=1, username="zzzz", client_state="client", name="ZZZZ", age=24,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=2, username="zzz", client_state="client", name="ZZZ", age=28,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=3, username="zz", client_state="client", name="ZZ", age=26,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=4, username="z", client_state="client", name="Z", age=24,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=5, username="ggggg", client_state="client", name="GGGGG", age=27,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=6, username="gggg", client_state="client", name="GGGG", age=23,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=7, username="ggg", client_state="client", name="GGG", age=21,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=8, username="gg", client_state="client", name="GG", age=26,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=9, username="g", client_state="client", name="G", age=30,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=10, username="fffff", client_state="client", name="FFFFF", age=20,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=11, username="ffff", client_state="client", name="FFFF", age=23,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=12, username="fff", client_state="client", name="FFF", age=29,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=13, username="ff", client_state="client", name="FF", age=18,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=14, username="f", client_state="client", name="F", age=21,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=15, username="eeeee", client_state="client", name="EEEEE", age=26,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=16, username="eeee", client_state="client", name="EEEE", age=27,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=17, username="eee", client_state="client", name="EEE", age=28,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=18, username="ee", client_state="client", name="EE", age=29,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=19, username="e", client_state="client", name="E", age=30,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=20, username="wwwww", client_state="client", name="WWWWW", age=34,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=21, username="wwww", client_state="client", name="WWWW", age=25,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=22, username="www", client_state="client", name="WWW", age=24,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=23, username="ww", client_state="client", name="WW", age=31,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()

    await UserDB(user_id=24, username="w", client_state="client", name="W", age=33,
                 gender="Женщина", biography=r'''Биогра́фия[1] (др.-греч. βίος — жизнь + γράφω — пишу; букв. 
                 «жизнеописание») — описание жизни человека, сделанное другими людьми или им самим (автобиография).
                 Биография включает в себя не только основные факты (Биографический факт) жизни, такие как рождение, 
                 происхождение, образование, служба, работа, семейные отношения и смерть; она также изображает опыт 
                 человека во время событий его жизни. В отличие от профиля или автобиографии (резюме), биография 
                 представляет историю жизни субъекта, выделяя различные аспекты его жизни, в том числе интимных 
                 подробностей, и может включать в себя анализ личности субъекта.''', latitude=59.848311,
                 longitude=30.361708, search_gender="Мужчина",
                 photo=user_photo,
                 search_age=[20, 30], search_latitude=59.848311, search_longitude=30.361708, search_radius=20,
                 users_i_liked=[], who_liked_me=[], mutual_liking=[]).create()
