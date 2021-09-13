from abc import ABC, abstractmethod
from typing import List

from cell import Cell
from board import Board


class ConstraintSolver(ABC):

    solution: Board = None
    hash_map: dict[int] = {bool}
    steps_taken: int = 0

    @abstractmethod
    def solve_csp(self, board: Board) -> bool:
        pass

    @abstractmethod
    def queueing_function(self, board: Board) -> List[Cell, int]:
        pass

    def print_output(self) -> None:
        pass




