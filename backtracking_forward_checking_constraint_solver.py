import board
from backtracking_constraint_solver import *
from board import *


class ForwardChecking(BacktrackingConstraintSolver):

    def solve_csp(self, board: Board) -> bool:
        if self.recursive_backtrack(board, 0):
            print("Found a solution in", self.steps_taken, "steps.")
        else:
            print("Exited before finding a solution.")

        return self.steps_taken

    def recursive_backtrack(self, board: Board, depth: int) -> bool:
        self.steps_taken += 1
        depth += 1

        status = board.check_success()
        if status == Status.SUCCESS:
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board)

            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell.location, value, False)

                for row in child.grid:
                    for cell in row:
                        if cell.value == 0 and len(cell.possible_values) == 0:
                            return False

                if self.recursive_backtrack(child, depth + 1):
                    return True
            return False