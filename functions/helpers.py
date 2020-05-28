from typing import Dict, List
from itertools import combinations


def find_all_allocation_options(nUsers: int, nChannels: int) -> Dict:
    "This function finds all possible user allocations for the different number of user and channel combinations."
    all_user_allocations = list(combinations([index for index in range(1, nUsers + 1)], nChannels))
    return {index: users for index, users in enumerate(all_user_allocations)}


def linearsearch(indices: List[int], user: int, nUsers: int, nChannels: int) -> [List[int], bool]:
    "This function performs a linear search on a list of integers to find a given integer."
    all_user_allocations: Dict = find_all_allocation_options(nUsers, nChannels)
    period: int = len(indices)
    _indices: List[int] = 2 * indices
    _time: List[int] = 2 * period * [0]
    k: int = 0
    flag: bool = False  # user cannot be found
    for index, element in enumerate(_indices):
        if any([True if i == user else False for i in all_user_allocations[element]]):
            k: int = 0
            flag: bool = True  # user is found
        else:
            k += 1
        _time[index] = k
    return _time[period:2 * period], flag


def index2schedule(indices: List[int], nUsers: int, nChannels: int) -> List[int]:
    "This function converts a list of indices to a list of scheduling actions."
    all_user_allocations = find_all_allocation_options(nUsers, nChannels)
    return [all_user_allocations[index] for index in indices]


def create_complete_search_tree(cardinality: int, period: int) -> List[int]:
    "This function creates a complete search tree."
    schedules = [[0] * period for i in range(cardinality ** period)]
    for j in range(period):
        k: int = 0
        for i in range(0, cardinality**period):
            schedules[i][j] = k % cardinality
            if i % (cardinality ** (period - 1 - j)) == 0: k += 1
    return schedules
