import random
import threading
from random import randrange
from math import exp
from threading import Thread

from constraint_solver import *
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
    https://www.bogotobogo.com/python/Multithread/python_multithreading_creating_threads.php
    """

    def __init__(self):
        self.starting_temperature: int = 1000000
        self.number_iterations: int = 5000
        self.debug = False
        self.solutions: List[Board] = []

    def __str__(self):
        return "Simulated annealing"

    def solve_csp(self, board: Board, *, _threading: bool = False) -> bool:
        """
        Implements Simulated Annealing to solve the board Board.
        :param board: A unsolved sudoku board as a Board
        :param _threading: A bool to determine whether or not to implement multithreading for this method call.
        :return: bool representing the success of solving board before the Temperature is less than 1 or the preset number of iterations is reached. If a solution is found returns True otherwise False.
        """
        print(self.__class__.__name__)
        if _threading is True:
            threads: List[Thread] = []
            non_solutions: List[Board] = []
            thread_count: int = 25
            for i in range(0, thread_count):
                threads.append(threading.Thread(target=self.simulated_annealing, args=(deepcopy(board),),
                                                name=f"simulated_annealing_thread{i}"))
            for thread in threads:
                thread.start()
            print(f"Threads 0-{thread_count - 1} started")
            for thread in threads:
                thread.join()
            print(f"Threads 0-{thread_count - 1} joined")
            for solution in self.solutions:
                if solution.value != 0:
                    non_solutions.append(solution)
            for board in non_solutions:
                self.solutions.remove(board)
            solution_probability: float = len(self.solutions) / len(threads)
            self.solution = self.solutions[0] if len(self.solutions) > 0 else None
            self.print_output(self.solution)
            print(f"Number of solutions: {len(self.solutions)}")
            print(f"Probability of generating a solution: {solution_probability*100}% with {thread_count} threads\n")
            return True if len(self.solutions) > 0 else False
        else:
            self.solution = self.simulated_annealing(deepcopy(board))
            self.print_output(self.solution)
            return True if self.solution.value == 0 else False

    def schedule(self, iteration_number: int) -> float:
        """
        Cooling Schedule for Simulated Annealing.
        :param iteration_number: current iteration from Simulated Annealing.
        :return:
        """
        tau: float = 99
        return (self.starting_temperature * tau) / (tau + iteration_number)

    def simulated_annealing(self, board: Board) -> Board:
        """
        Implementation of Simulated Annealing
        :param board: Unsolved Sudoku board represented as a Board
        :return: Board as a solution. If the Board is not solves, returns current progress.
        """
        k_boltzmann_constant: float = 0.00001
        current_board = board
        for t in range(1, self.number_iterations):
            temperature: float = self.schedule(t)
            if temperature < 0.0000001 or t == self.number_iterations - 1 or current_board.value == 0:
                if current_board.value == 0:
                    print(t)
                self.solutions.append(deepcopy(current_board))
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
                current_board = \
                    random.choices([current_board, next_board], weights=[1, next_board_probability * 100], k=1)[0]

    @staticmethod
    def random_neighbor(current_board) -> Board:
        """
        Static method used to randomly change the value of one cell in current board.
        :param current_board: Current state of a Sudoku board represented as a Board from Simulated Annealing
        :return: Next possible board for Simulated Annealing
        """
        preselected: bool = True
        new_board: Board = deepcopy(current_board)
        while preselected:
            cell: Cell = deepcopy(current_board.grid[randrange(9)][randrange(9)])
            if not cell.preset and new_board.cell_value(cell) != 0:
                preselected = False
                cell.value = random.choice(cell.possible_values)
                new_board.grid[cell.location[0]][cell.location[1]] = cell
        return new_board
