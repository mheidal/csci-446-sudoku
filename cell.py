from typing import List


class Cell:

    location: List[int] = {int, int}
    value: int = 0
    possible_values: List[int] = None

    def __init__(self, loc, val):
        self.value = val
        self.location = loc

    def __str__(self):
        return f"row:{self.location[0]}; column:{self.location[1]}; value:{self.value}"
