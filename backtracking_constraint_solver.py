from board import *
from constrain_solver import *


# An abstract class which solves sudoku puzzles using backtracking depth-first search via recursion.
# Inheritor classes must implement the recursive_backtracking method, but may use this class's implementation
# of solve_csp and queueing_function.
# Local variables:
# - steps_taken: int -- records the number of 'core' function calls, i.e. the number of recursive calls

class BacktrackingConstraintSolver(ConstraintSolver):

    # A method which serves as the first step of the recursive solving process. Initializes steps_taken and recursive
    # calls.
    # Parameters:
    # - board: Board -- the initial board state.
    # Returns:
    # - bool -- represents whether the algorithm successfully found a solution to the input puzzle.
    def solve_csp(self, board: Board) -> bool:
        self.steps_taken = 0
        done = self.recursive_backtrack(board)
        print("Found solution in", self.steps_taken, "steps.")
        return done

    # The core method used by backtracking search algorithms.
    # Parameters:
    # - board: Board -- the board state to analyze and alter in this step of the recursive process.
    # Returns:
    # - bool -- represents whether the board state passed in is either a successful state or part of the path to a
    #           successful state, or if the board contains contradictions or is not part of the path to a successful
    #           state.
    @abstractmethod
    def recursive_backtrack(self, board: Board) -> bool:
        pass

    # A method which analyzes a board state and decides the order in which to try to insert values. Used as a helper
    # method for the core method. This implementation of the queueing function returns a list of all values which can
    # possibly be assigned to a single cell, given current constraints. It chooses to return the cell which has the
    # fewest such values.
    # Parameters:
    # - board: Board -- the board state to analyze.
    # Returns:
    # - List[Tuple[Cell, int]] -- A list of tuples, each of which contains a cell to insert a value into and a value
    #                             to insert into that cell.
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
