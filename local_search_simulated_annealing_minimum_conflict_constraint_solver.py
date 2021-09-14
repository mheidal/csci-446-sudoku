from constrain_solver import *
from board import *


class LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver(ConstraintSolver):
    """
    Simulated Annealing:
        - Minor variation of HillClimbing
        - Occasionally make a 'bad' choice based on current temperature (T)
        -
    Minimum Conflict: Chooses new var val that results in the minimum number of conflicts with other vars.

    https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.216.3484&rep=rep1&type=pdf
    """

    def __init__(self):
        self.starting_temperature: int = 1000000

    def queueing_function(self, board: Board) -> List[Cell, int]:
        pass

    def solve_csp(self, board: Board) -> bool:
        pass

    def schedule(self, iteration_number: int) -> float:
        tau: float = 1.0
        return (self.starting_temperature * tau)/(tau + iteration_number)

    def make_node(self, board: Board) -> Board:
        """

        :return:
        """
        return board

    def simulated_annealing(self, board, schedule):
        """
        VALUE(node) is the current value of the board such that value is 1 divided by the number of violated states for the current node. Value should be in Board
        :param board:
        :param schedule:
        :return:
        """
        current_board = None
        next_board = None
        temperature = None
        energy = None
        k_boltzmann_constant: float = 1.38*pow(10, -23)
        current_board = self.make_node(board)
        for t in range(1, self.starting_temperature):
            temperature = self.schedule(t)
            if temperature == 0:
                return current_board
            next_board = self.random_neighbor(current_board)

    def random_neighbor(self, current_board):
        return current_board
