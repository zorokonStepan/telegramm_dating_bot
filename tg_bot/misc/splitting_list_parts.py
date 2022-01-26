# генератор для разбиения списка на части.
def func_chunks_generators(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]
