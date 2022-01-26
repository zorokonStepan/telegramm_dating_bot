"""Функции для вывода разности времени"""


# def timedelta_to_hms(duration):
#     # преобразование в часы, минуты и секунды
#     days, seconds = duration.days, duration.seconds
#     hours = days * 24 + seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = (seconds % 60)
#     return hours, minutes, seconds


# def timedelta_to_dhms(duration):
#     # преобразование в дни, часы, минуты и секунды
#     days, seconds = duration.days, duration.seconds
#     hours = seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = (seconds % 60)
#     return days, hours, minutes, seconds


def timedelta_to_h(duration):
    # преобразование в часы
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    return hours
