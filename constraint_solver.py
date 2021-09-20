from abc import ABC, abstractmethod
from typing import List
from typing import Tuple

from cell import Cell
from board import Board
from copy import deepcopy

# Abstract class inherited by all constraint satisfaction problem solving algorithms.
# Attributes:
# - steps_taken: the number of 'core' method calls used when solving a CSP.
class ConstraintSolver(ABC):

    steps_taken: int = 0

    # Abstract method used to initialize the CSP solving process in each child algorithm.
    @abstractmethod
    def solve_csp(self, board: Board) -> bool:
        pass

    # Utility method to print the solution to the CSP when found.
    def print_output(self, board: Board) -> None:
        print(board)
