from typing import List
from typing import Tuple

class Cell:

    def __init__(self, loc: Tuple[int, int], val: int = 0, preset: bool = False):
        self.location: Tuple[int, int] = loc
        self.value = val
        self.preset = preset
        self.possible_values: List[int] = []
        if not preset:
            self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return

    def __str__(self):
        return f"row:{self.location[0]}; column:{self.location[1]}; value:{self.value}; predetermined:{self.preset}"

    def set_possible_values(self, poss) -> None:
        self.possible_values = poss
        return

    def get_row_index(self) -> int:
        return self.location[0]

    def get_col_index(self) -> int:
        return self.location[1]

    # TODO: THERE'S A MORE ELEGANT WAY TO DO THIS
    def get_box_index(self) -> int:
        if self.location[0] % 3 == 0:
            if self.location[1] % 3 == 0:
                return 0
            elif self.location[1] % 3 == 1:
                return 1
            elif self.location[1] % 3 == 2:
                return 2
        if self.location[0] % 3 == 1:
            if self.location[1] % 3 == 0:
                return 3
            elif self.location[1] % 3 == 1:
                return 4
            elif self.location[1] % 3 == 2:
                return 5
        if self.location[0] % 3 == 2:
            if self.location[1] % 3 == 0:
                return 6
            elif self.location[1] % 3 == 1:
                return 7
            elif self.location[1] % 3 == 2:
                return 8
