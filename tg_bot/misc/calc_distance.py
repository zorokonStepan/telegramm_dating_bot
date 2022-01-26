from math import radians, pi, sin, cos, asin, sqrt, ceil

'''две равнозначные функции для подсчета удаленности относительно заданного радиуса'''
R = 6378.1


def calc_distance_func(latitude: float, longitude: float, search_latitude: float, search_longitude: float):
    latitude, longitude, search_latitude, search_longitude = \
        map(radians, [latitude, longitude, search_latitude, search_longitude])
    # haversine formula
    dlon = search_longitude - longitude
    dlat = search_latitude - latitude
    a = sin(dlat / 2) ** 2 + cos(latitude) * cos(search_latitude) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return ceil(km)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
    # расстояние между широтами и долготы
    dLat = (lat2 - lat1) * pi / 180.0
    dLon = (lon2 - lon1) * pi / 180.0
    # преобразовать в радианы
    lat1 = (lat1) * pi / 180.0
    lat2 = (lat2) * pi / 180.0
    # применять формулы
    a = (pow(sin(dLat / 2), 2) + pow(sin(dLon / 2), 2) * cos(lat1) * cos(lat2))
    rad = 6371
    c = 2 * asin(sqrt(a))
    return ceil(rad * c)


# проверка работы функций
if __name__ == "__main__":
    lat1 = 51.528308

    lon1 = -0.3817765

    lat2 = 40.6971494

    lon2 = -74.2598661

    print(haversine(lat1, lon1, lat2, lon2), "K.M.")
    print(calc_distance_func(lat1, lon1, lat2, lon2), "K.M.")
    # 5571 км (по прямой)
    # Нью-Йорк — Лондон
