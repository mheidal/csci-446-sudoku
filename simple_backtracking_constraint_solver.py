from typing import List
from board import Board
from cell import Cell
from backtracking_constraint_solver import *


# Child class of BacktrackingConstraintSolver. This sudoku solver recursively assigns values to cells in an essentially
# random order, choosing cells row by row and column by column, attempting to assign the values 1 through 9 to each
# cell.
class SimpleBacktracking(BacktrackingConstraintSolver):

    def __str__(self):
        return "Simple backtracking"

    # Implementation of abstract method from parent class. This method:
    # 1. Tests if the board state it is given as an argument is in a success state, a failure state, or neither.
    #    If the board is in a success state, it returns True; if the board is in a failure state, it returns False.
    # 2. Gets a list of cell and value assignment pairs from the queuing function helper method.
    # 3. Makes a copy of the board for each cell-value pair and recurses. If that new board assignment is
    #    successful, the method returns True. If no cell-value pair given by the queuing function is successful or a
    #    step on the path to a successful state, the method returns False.
    # Parameters:
    # - board: Board -- a potential board state to be analyzed and either accepted, discarded or inserted into.
    # - method: QueuingType -- which queuing strategy to use. Passed on as a parameter to queuing_function.
    # Returns:
    # - bool -- represents whether or not this board is or is a step on the path to a successful board state.
    def recursive_backtrack(self, board: Board, method: QueuingType) -> bool:
        self.steps_taken += 1

        print(board)

        status = board.check_success()

        if status == Status.SUCCESS:
            self.print_output(board)
            return True
        elif status == Status.FAILURE:
            return False
        else:
            order = self.queueing_function(board, method)
            for cell, value in order:
                child = deepcopy(board)
                child.insert_value(cell, value, False)
                if self.recursive_backtrack(child, method):
                    return True

            return False
