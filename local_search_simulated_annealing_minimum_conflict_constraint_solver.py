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
    http://rhydlewis.eu/papers/META_CAN_SOLVE_SUDOKU.pdf
    """

    def __init__(self):
        self.starting_temperature: int = 1000000
        self.number_iterations: int = 2500
        self.debug = False

    def queueing_function(self, board: Board):
        pass

    def solve_csp(self, board: Board) -> bool:
        print(self.__class__.__name__)
        #self.solution = self.simulated_annealing(board=board)
        self.solution = self.simulated_annealing_v2(board=board)
        self.print_output(self.solution)
        return True

    @staticmethod
    def starting_board(_board: Board) -> Board:
        board = deepcopy(_board)
        for block in board.get_box_list():
            domain: List[int] = deepcopy(board.domain)
            not_preset_cells: List[Cell] = []
            for cell in block:
                if cell.preset:
                    domain.remove(cell.value)
                else:
                    not_preset_cells.append(cell)
            random.shuffle(not_preset_cells)
            for cell in not_preset_cells:
                cell.value = random.choice(domain)
                domain.remove(cell.value)
        return board

    def schedule(self, iteration_number: int) -> float:
        tau: float = 99  # controls curvature of the graph of the temperature over iterations
        return (self.starting_temperature * tau) / (tau + iteration_number)

    @staticmethod
    def simple_schedule(current_temperature: float):
        alpha: float = 0.99
        return current_temperature * alpha

    def simulated_annealing(self, board: Board) -> Board:
        """
        :param board:
        :return:
        """
        # k_boltzmann_constant: float = 1.0
        k_boltzmann_constant: float = 0.00001
        # k_boltzmann_constant: float = 1.38*pow(10, -23)
        current_board = board
        for t in range(1, self.number_iterations):
            temperature: float = self.schedule(t)
            if temperature < 0 or t == self.number_iterations - 1 or current_board.value == 0:
                print(
                    f"\nSimulated Annealing\nViolated Constraints: {current_board.value}\nNumber of Iterations: {t}\nCurrent Temperature: {temperature}\n")
                return current_board  # if current_board.value == 0 else self.simulated_annealing(deepcopy(current_board))
            next_board: Board = self.random_neighbor(current_board)
            delta_energy: int = (next_board.value - current_board.value) * -1
            if delta_energy > 0:  # if the number of violated constrains in current is greater than that in next
                current_board = next_board
            elif delta_energy != 0:
                next_board_probability: float = 0
                try:
                    next_board_probability = 1 / (
                        exp((-delta_energy) / (k_boltzmann_constant * temperature)))
                except OverflowError:
                    next_board_probability = 0.01
                # next_board_probability: float = 0 if (delta_energy == 0) and (temperature < self.starting_temperature/2) else 1 / (exp((-delta_energy) / (k_boltzmann_constant * temperature)))
                current_board = \
                    random.choices([current_board, next_board], weights=[1, next_board_probability * 100], k=1)[0]

    def simulated_annealing_v2(self, board: Board) -> Board:
        k_boltzmann_constant: float = 0.00001
        current_board = self.starting_board(board)
        t: int = 0
        temperature: float = self.starting_temperature
        print(current_board)
        while t > 0:
            temperature = self.simple_schedule(temperature) if t > 0 else temperature
            if temperature <= 0 or current_board.value == 0:
                print(
                    f"\nSimulated Annealing\nViolated Constraints: {current_board.value}\nNumber of Iterations: {t}\nCurrent Temperature: {temperature}\n")
                return current_board  # if current_board.value == 0 else self.simulated_annealing(deepcopy(current_board))
            next_board: Board = self.random_neighbor_v2(current_board)
            delta_energy: int = (next_board.value - current_board.value) * -1
            if delta_energy > 0:  # if the number of violated constrains in current is greater than that in next
                current_board = next_board
            elif delta_energy != 0:
                next_board_probability: float = 0
                try:
                    next_board_probability = 1 / (
                        exp((-delta_energy) / (k_boltzmann_constant * temperature)))
                except OverflowError:
                    next_board_probability = 0.01
                # next_board_probability: float = 0 if (delta_energy == 0) and (temperature < self.starting_temperature/2) else 1 / (exp((-delta_energy) / (k_boltzmann_constant * temperature)))
                current_board = \
                    random.choices([current_board, next_board], weights=[1, next_board_probability * 100], k=1)[0]

    def random_neighbor(self, current_board) -> Board:
        preselected: bool = True
        new_board: Board = deepcopy(current_board)
        # new_board.grid = deepcopy(current_board.grid)
        while preselected:
            cell: Cell = deepcopy(current_board.grid[randrange(9)][randrange(9)])
            if not cell.preset and new_board.cell_value(cell) != 0:
                preselected = False
                orig_val: int = cell.value
                cell.value = random.choice(cell.possible_values)
                new_board.grid[cell.location[0]][cell.location[1]] = cell
                if self.debug is True:
                    print(f"Cell at [{cell.location[0]}][{cell.location[1]}] changed from {orig_val} to {cell.value}")
        return new_board

    def random_neighbor_v2(self, current_board) -> Board:
        preselected: bool = True
        new_board: Board = deepcopy(current_board)
        cell: Cell = Cell((0, 0))
        while preselected:
            cell: Cell = deepcopy(current_board.grid[randrange(9)][randrange(9)])
            if not cell.preset:
                preselected = False
        block = current_board.block(cell)
        block.remove(cell)
        other_cell: Cell = deepcopy(random.choice(block))
        temp_cell: Cell = deepcopy(other_cell)
        if self.debug is True:
            print(f"Cell at [{cell.location[0]}][{cell.location[1]}]: {cell}")
            print(f"Cell at [{other_cell.location[0]}][{other_cell.location[1]}]: {other_cell}")
        new_board.grid[other_cell.location[0]][other_cell.location[1]] = cell
        new_board.grid[cell.location[0]][cell.location[1]] = temp_cell
        if self.debug is True:
            print(f"Cell at [{cell.location[0]}][{cell.location[1]}]: {new_board.grid[temp_cell.location[0]][temp_cell.location[1]]}")
            print(f"Cell at [{temp_cell.location[0]}][{temp_cell.location[1]}]: {new_board.grid[cell.location[0]][cell.location[1]]}")
        return new_board
