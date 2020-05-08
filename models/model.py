from copy import deepcopy
from typing import List, Callable


# tag::schedule[]
class Schedule:
    def __init__(self, sequence: List[int], func: Callable[[
                 List[int]], float], period: int, no_users: int) -> None:
        self.period: int = period
        self.no_users: int = no_users
        self.func: Callable[[List[int]], float] = func
        self.sequence: List[int] = sequence

    def legal_choices(self) -> List[int]:
        if self.is_over():
            return []
        return [i for i in range(1, self.no_users + 1)]

    def allocate(self, user: int) -> object:
        new_sequence = deepcopy(self.sequence)
        new_sequence.append(user)
        return Schedule(new_sequence, self.func, self.period, self.no_users)

    def evaluate(self) -> float:
        return self.func(self.sequence)

    def is_over(self) -> bool:  # is_completed
        return len(self.sequence) >= self.period

    def __str__(self) -> str:  # needed to be updated
        return f"The schedule is {self.sequence} that is {self.is_over()}."
# end::schedule[]
