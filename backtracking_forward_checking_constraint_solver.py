import board
from backtracking_constraint_solver import *
from board import *

# Child class of BacktrackingConstraintSolver. This sudoku solver recursively assigns values to cells in an order
# chosen by the parent class's queuing function, checking after every insertion whether any cell has no possible
# values left for it to choose.
class ForwardChecking(BacktrackingConstraintSolver):

    # Implementation of abstract method from parent class. This method:
    # 1. Tests if the board state it is given as an argument is in a success state, a failure state, or neither.
    #    If the board is in a success state, it returns True; if the board is in a failure state, it returns False.
    # 2. Gets a list of cell and value assignment pairs from the queuing function helper method.
    # 3. Makes a copy of the board for each cell-value pair and recurses. If that new board assignment is
    #    successful, the method returns True. If no cell-value pair given by the queuing function is successful or a
    #    step on the path to a successful state, the method returns False.
    # 4. Checks whether there are any cells which have constraints restricting them from having any possible values.
    #    If any such cells exist, the method returns False, as the board is in a failure state.
    #    For example, if two cells in the same row can only be assigned the value 9 without violating a constraint,
    #    assigning 9 to either would cause the board to enter a failure state.
    # Parameters:
    # - board: Board -- a potential board state to be analyzed and either accepted, discarded or inserted into.
    # Returns:
    # - bool -- represents whether or not this board is or is a step on the path to a successful board state.
    def recursive_backtrack(self, board: Board) -> bool:
        self.steps_taken += 1

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
                child.insert_value(cell, value, False)

                for row in child.grid:
                    for entry in row:
                        if entry.value == 0 and len(entry.possible_values) == 0:
                            return False

                if self.recursive_backtrack(child):
                    return True
            return False
