from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    def solve_csp(self, board: Board, method: int = 0) -> bool:
        self.recursive_backtrack(board, 0, method)
        return self.steps_taken

    @abstractmethod
    def recursive_backtrack(self, board: Board, depth: int, method) -> bool:
        pass

    # Methods/heuristics:
    # - In order of ascending x-index, then y-index. (Arbitrary order)
    # - - Key: 0
    # - In order of acending number of constraints (reverse degree heuristic)
    # -- Key: 1
    # TODO: IMPLEMENT MORE, ASSESS COMPARATIVELY?
    def queueing_function(self, board: Board, method: int = 0) -> List[Tuple[Cell, int]]:
        if method == 0:
            queue = []
            for row in board.grid:
                for cell in row:
                    if cell.value == 0:
                        for i in range(1, 10, 1):
                            queue.append((cell, i))
                        return queue
        elif method == 1:
            cell_with_most_constraints: Cell = None
            greatest_constraint_value: float = float('inf')
            for row in board.grid:
                for cell in row:
                    if cell.value == 0:
                        neighbors = board.get_cells_with_constraint(cell)
                        if len(neighbors) < greatest_constraint_value:
                            greatest_constraint_value = len(neighbors)
                            cell_with_most_constraints = cell
            queue = []
            for i in range(1, 10, 1):
                queue.append((cell_with_most_constraints, i))
            return queue
