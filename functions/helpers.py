import numpy as np


def linearsearch(sequence: np.ndarray,
                 key_element: int) -> [np.ndarray, bool]:
    "Perform a linear search on an array for a given element."
    period: int = len(sequence)
    _sequence: np.ndarray = np.tile(sequence, 2)  # double up the sequence
    _time: np.ndarray = np.zeros((2 * period,), dtype=int)
    k: int = 0
    flag: bool = False  # key_element cannot be found
    for index, element in enumerate(_sequence):
        if element == key_element:
            k: int = 0
            flag: bool = True  # key_element is found
        else:
            k += 1
        _time[index] = k
    return _time[period:2 * period], flag


def allschedules(N: int, T: int) -> np.ndarray:
    "Create a complete search tree. `N` is the number of plants and `T` is the period."
    schedules: np.ndarray = np.zeros((np.power(N, T), T), dtype=int)
    for j in range(T):
        k: int = 0
        for i in range(0, N ** T, N ** (T - 1 - j)):
            schedules[i:(i + N ** (T - 1 - j)), j] = (k % N) + 1
            k += 1
    return schedules
