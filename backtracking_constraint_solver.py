from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    # TODO
    def __init__(self):
        return

    def solve_csp(self, board: Board) -> bool:
        return self.recursive_backtrack(board)

    def recursive_backtrack(self, board) -> bool:
        self.steps_taken += 1
        #TODO: DEBUG MESSAGE
        print(self.steps_taken)

        status = board.check_success()
        if status == Status.SUCCESS:
            print("Found success state.")
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            print("Found dead end.")
            return False
        else:
            order = self.queueing_function(board)
            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell.location, value)

                if self.recursive_backtrack(child):
                    return True

            return False

    # Method: minimum remaining values.
    # TODO: IMPLEMENT MORE, ASSESS COMPARATIVELY?
    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        temp = []
        for row in board.grid:
            for cell in row:
                temp.append(deepcopy(cell))
        # for y in temp:
        #     print(y.possible_values)
        # sorted(temp, key=lambda x: len(x.possible_values))

        out = []
        for cell in temp:
             for val in cell.possible_values:
                 out.append((cell, val))
        return out