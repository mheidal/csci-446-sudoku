from typing import List


class Cell:

    location: List[int] = {int, int}
    value: int = 0
    possible_values: List[int] = None

    def __init__(self, loc, val = 0):
        self.location = loc
        self.value = val
        return

    def set_possible_values(self, poss) -> None:
        self.possible_values = poss
        return
