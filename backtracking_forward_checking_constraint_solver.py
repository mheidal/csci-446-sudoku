import board
from backtracking_constraint_solver import *
from board import *


class ForwardChecking(BacktrackingConstraintSolver):

    def solve_csp(self, board: Board) -> bool:
        board.initialize_possible_values()
        if self.recursive_backtrack(board, 0):
            print("Found a solution.")
        else:
            print("Exited before finding a solution.")

        return self.steps_taken

    def recursive_backtrack(self, board: Board, depth: int) -> bool:
        self.steps_taken += 1
        depth += 1

        status = board.check_success()

        if status == Status.SUCCESS:
            print("found successful state")
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board)

            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell.location, value, False)

                if not child.update_possible_values(child[cell.location[0], cell.location[0]]):
                    return False

                elif self.recursive_backtrack(child, depth):
                    return True

            return False

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