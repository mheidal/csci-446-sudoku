from board import *
from constraint_solver import *


class QueuingType(Enum):
    ARBITRARY = 0
    MINIMUM_REMAINING_VALUES = 1
    DEGREE_HEURISTIC = 2
    LEAST_CONSTRAINING_VALUE = 3



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
    def solve_csp(self, board: Board, method: QueuingType = QueuingType.MINIMUM_REMAINING_VALUES) -> bool:
        self.steps_taken = 0
        done = self.recursive_backtrack(board, method)
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
    # method for the core method.
    # Each method selects a single cell, then returns a list of cell-value pairs containing that cell paired with every
    # one of its possible values.
    # Parameters:
    # - board: Board -- the board state to analyze.
    # - method: QueuingType -- the queuing function to select. There are four such methods.
    # Returns:
    # - List[Tuple[Cell, int]] -- A list of tuples, each of which contains a cell to insert a value into and a value
    #                             to insert into that cell.
    def queueing_function(self, board: Board, method: QueuingType) -> List[Tuple[Cell, int]]:

        # This implementation of the queuing function selects the first cell it finds going row-by-row and column-
        # by-column.
        if method == QueuingType.ARBITRARY:
            queue = []
            for row in board.grid:
                for cell in row:
                    if cell.value == 0:
                        for value in cell.possible_values:
                            queue.append((cell, value))
                        return queue

        # This implementation of the queuing function selects the cell which has the fewest values in its domain.
        elif method == QueuingType.MINIMUM_REMAINING_VALUES:
            cell_with_fewest_possible_values: Cell = None
            fewest_possible_values: float = float('inf')
            for row in board.grid:
                for cell in row:
                    if len(cell.possible_values) != 0 and len(cell.possible_values) < fewest_possible_values:
                        cell_with_fewest_possible_values = cell
                        fewest_possible_values = len(cell.possible_values)
            queue = []
            for value in cell_with_fewest_possible_values.possible_values:
                queue.append((cell_with_fewest_possible_values, value))
            return queue

        # This implementation of the queuing function selects the cell involved in the largest number of constraints.
        elif method == QueuingType.DEGREE_HEURISTIC:
            cell_with_most_neighbors: Cell = None
            most_neighbors: float = -1
            for row in board.grid:
                for cell in row:
                    if cell.value == 0:
                        neighbors = board.get_cells_with_constraint(cell)
                        num_unassigned_neighbors: int = 0
                        for neighbor in neighbors:
                            if neighbor.value == 0:
                                num_unassigned_neighbors += 1
                        if num_unassigned_neighbors > most_neighbors:
                            most_neighbors = num_unassigned_neighbors
                            cell_with_most_neighbors = cell
            queue = []
            for value in cell_with_most_neighbors.possible_values:
                queue.append((cell_with_most_neighbors, value))
            return queue

        # This implementation of the queuing function selects the cell which has the value in its domain which
        # eliminates the fewest values in the domains of the cell's neighbors.
        elif method == QueuingType.LEAST_CONSTRAINING_VALUE:
            cell_with_least_constraining_value: Cell = None
            least_constraints: int = float('inf')
            for row in board.grid:
                for cell in row:
                    neighbors = board.get_cells_with_constraint(cell)
                    for value in cell.possible_values:
                        num_constraints_involved: int = 0
                        for neighbor in neighbors:
                            if value in neighbor.possible_values:
                                num_constraints_involved += 1
                        if least_constraints > num_constraints_involved:
                            least_constraints = num_constraints_involved
                            cell_with_least_constraining_value = cell
            queue = []
            for value in cell_with_least_constraining_value.possible_values:
                queue.append((cell_with_least_constraining_value, value))
            return queue
