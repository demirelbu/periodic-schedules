from copy import deepcopy
from typing import List, Callable
from itertools import combinations


class Schedule:
    def __init__(self, sequence: List[int], func: Callable[[
                 List[int]], float], period: int, nUsers: int, nChannels: int) -> None:
        self.period: int = period
        self.nUsers: int = nUsers
        self.nChannels: int = nChannels
        self._sequence: List[int] = sequence
        self.func: Callable[[List[int]], float] = func

    @property
    def allocation_options(self) -> List[int]:
        return list(combinations(
            [index for index in range(1, self.nUsers + 1)], self.nChannels))

    @property
    def allocation_options_masked(self) -> List[int]:
        if self.is_maximum_cardinality_reached:
            return []
        else:
            return [index for index in range(len(self.allocation_options))]

    def allocate(self, user: int) -> object:
        new_sequence = deepcopy(self._sequence)
        new_sequence.append(user)
        return Schedule(new_sequence, self.func, self.period,
                        self.nUsers, self.nChannels)

    @property
    def evaluate(self) -> float:
        return self.func(self._sequence)

    @staticmethod
    def normalize(value: float, max_value: float = 10000.0) -> float:
        if value > max_value:
            return 0.0
        else:
            return 1 - value / max_value

    @property
    def schedule(self) -> List[int]:
        all_user_allocations = {
            index: users for index,
            users in enumerate(self.allocation_options)}
        return [all_user_allocations[index] for index in self._sequence]

    @property
    def is_maximum_cardinality_reached(self) -> bool:
        return len(self._sequence) >= self.period

    def __str__(self) -> str:
        return f"For the communication sequence of {self.schedule}, the control cost is computed as {self.evaluate}."
