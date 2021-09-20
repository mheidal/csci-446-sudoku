from typing import List

from board import Board

from cell import Cell

from backtracking_constraint_solver import *

# Child class of BacktrackingConstraintSolver. This sudoku solver recursively assigns values to cells in an essentially
# random order, choosing cells row by row and column by column, attempting to assign the values 1 through 9 to each
# cell.
class SimpleBacktracking(BacktrackingConstraintSolver):

    # Implementation of abstract method from parent class. This method:
    # 1. Tests if the board state it is given as an argument is in a success state, a failure state, or neither.
    #    If the board is in a success state, it returns True; if the board is in a failure state, it returns False.
    # 2. Gets a list of cell and value assignment pairs from the queuing function helper method.
    # 3. Makes a copy of the board for each cell-value pair and recurses. If that new board assignment is
    #    successful, the method returns True. If no cell-value pair given by the queuing function is successful or a
    #    step on the path to a successful state, the method returns False.
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
                if self.recursive_backtrack(child):
                    return True

            return False

    # A helper method which creates a list of cell-value pairs which the main method will attempt to insert into a board
    # state. Returns a list containing many copies of the same cell paired with the values 1 through 9. The cell
    # returned is the first cell found to have no value assigned to it, going row-by-row and column-by-column.
    # Parameters:
    # - board: Board -- a board state to select a cell from.
    # Returns:
    # - queue: List[Tuple[Cell, int]] -- a list of cell-value pairs.
    def queueing_function(self, board: Board) -> List[Tuple[Cell, int]]:
        queue = []
        for row in board.grid:
            for cell in row:
                if cell.value == 0:
                    for i in range(1, 10, 1):
                        queue.append((cell, i))
                    return queue
