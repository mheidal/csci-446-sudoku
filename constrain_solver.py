from abc import ABC, abstractmethod
from typing import List
from typing import Tuple

from cell import Cell
from board import Board
from copy import deepcopy


class ConstraintSolver(ABC):

    solution: Board = None
    hash_map: dict[int] = {bool}
    steps_taken: int = 0

    @abstractmethod
    def solve_csp(self, board: Board) -> bool:
        pass

    def print_output(self, board: Board) -> None:
        print(board)
        print(self.solution.value)
        return