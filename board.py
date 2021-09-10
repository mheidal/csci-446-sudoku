from enum import Enum
from typing import List

import np as np

from cell import Cell


class Status(Enum):
    SUCCESS = 1
    FAILURE = 2
    CONTINUE = 3


class Board:
    grid: List[Cell][Cell]

    def read_in_csv(self) -> None:
        pass

    def insert_value(self, cell: Cell, value: int) -> None:
        pass

    def hash_board(self) -> int:
        pass

    def check_success(self) -> Status:
        pass
