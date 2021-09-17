from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    def solve_csp(self, board: Board, method: int = 0) -> bool:
        self.steps_taken = 0
        self.recursive_backtrack(board, 0, method)
        return self.steps_taken

    @abstractmethod
    def recursive_backtrack(self, board: Board, depth: int, method) -> bool:
        pass


    @abstractmethod
    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        pass
