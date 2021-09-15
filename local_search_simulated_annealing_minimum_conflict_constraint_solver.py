import random
from random import randrange
from math import exp

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
        self.number_iterations: int = 10000
        self.debug = False

    def queueing_function(self, board: Board):
        pass

    def solve_csp(self, board: Board) -> bool:
        print(self.__class__)
        self.solution = self.simulated_annealing(board=board)
        self.print_output(self.solution)
        return True

    def schedule(self, iteration_number: int) -> float:
        tau: float = 50  # controls curvature of the graph of the temperature over iterations
        return (self.starting_temperature * tau) / (tau + iteration_number)

    def simulated_annealing(self, board: Board) -> Board:
        """
        :param board:
        :return:
        """
        k_boltzmann_constant: float = 0.00001
        # k_boltzmann_constant: float = 1.38*pow(10, -23)
        current_board = board
        for t in range(1, self.number_iterations):
            temperature: float = self.schedule(t)
            if temperature < 0 or t == self.number_iterations - 1:
                return current_board
            next_board: Board = self.random_neighbor(current_board)
            delta_energy: int = (next_board.value - current_board.value) * -1
            if delta_energy > 0:  # if the number of violated constrains in current is greater than that in next
                current_board = next_board
            else:
                next_board_probability: float = 1 / (
                    exp((-delta_energy) / (k_boltzmann_constant * temperature)))
                # next_board_probability: float = 0 if (delta_energy == 0) and (temperature < self.starting_temperature/2) else 1 / (exp((-delta_energy) / (k_boltzmann_constant * temperature)))
                current_board = \
                random.choices([current_board, next_board], weights=[1, next_board_probability * 100], k=1)[0]

    def random_neighbor(self, current_board) -> Board:
        preselected: bool = True
        new_board: Board = deepcopy(current_board)
        # new_board.grid = deepcopy(current_board.grid)
        while preselected:
            cell: Cell = deepcopy(current_board.grid[randrange(9)][randrange(9)])
            if not cell.preset:
                preselected = False
                orig_val: int = cell.value
                cell.value = random.choice(Board.domain)
                new_board.grid[cell.location[0]][cell.location[1]] = cell
                if self.debug is True:
                    print(f"Cell at [{cell.location[0]}][{cell.location[1]}] changed from {orig_val} to {cell.value}")
        return new_board
