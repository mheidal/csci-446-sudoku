from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    def solve_csp(self, board: Board) -> bool:
        self.steps_taken = 0
        done = self.recursive_backtrack((board))
        print("Found solution in", self.steps_taken, "steps.")
        return done

    @abstractmethod
    def recursive_backtrack(self, board: Board, depth: int) -> bool:
        pass

    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        cell_with_fewest_possible_values: Cell = None
        fewest_possible_values: float = float('inf')
        for row in board.grid:
            for cell in row:
                if len(cell.possible_values) != 0 and len(cell.possible_values) < fewest_possible_values:
                    cell_with_fewest_possible_values = cell
                    fewest_possible_values = len(cell.possible_values)
        output = []
        for value in cell_with_fewest_possible_values.possible_values:
            output.append((cell_with_fewest_possible_values, value))
        return output
