from board import *
from constrain_solver import *


class BacktrackingConstraintSolver(ConstraintSolver):

    # TODO
    def __init__(self):
        return

    def solve_csp(self, board: Board) -> bool:
        return self.recursive_backtrack(board, 0)

    def recursive_backtrack(self, board: Board, depth: int) -> bool:
        self.steps_taken += 1
        depth += 1

        status = board.check_success()

        #TODO: DEBUG MESSAGE
        print("steps", self.steps_taken)
        print("depth", depth)
        print("status", status)

        if status == Status.SUCCESS:
            print("Found success state.")
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            print("Found dead end.")
            return False
        else:
            order = self.queueing_function(board)

            #DEBUG MESSAGE
            string = ""
            for item in order:
                string += "[" + str(item[0].location) + ", " + str(item[1]) + "] | "
            print("The order in which insertions will be tested is")
            print(string)

            for cell, value in order:
                child = deepcopy(board)
                print("inserting", value, "to", cell.location, "- current board is")
                child.insert_value(cell.location, value, False)
                print(child)

                if self.recursive_backtrack(child, depth):
                    return True
                else:
                    print("backtracked to depth", depth)

            return False

    # Method: minimum remaining values.
    # TODO: IMPLEMENT MORE, ASSESS COMPARATIVELY?
    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        out = []
        for row in board.grid:
            for cell in row:
                if cell.value == 0:
                    for i in range(1, 10, 1):
                        out.append((deepcopy(cell), i))

        # for y in temp:
        #     print(y.possible_values)
        # sorted(temp, key=lambda x: len(x.possible_values))
        return out