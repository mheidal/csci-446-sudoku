from board import Board
from local_search_simulated_annealing_minimum_conflict_constraint_solver import LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver


def main():
    board: Board = Board()
    row = board.row(board.grid[3][4])
    column = board.column(board.grid[3][4])

    print(f"board[3][4]:\t{board.grid[3][4]}")
    print(f"row[0]:\t\t\t{row[0]}")
    print(f"column[0]:\t\t{column[0]}")
    print(f"board.value:\t{board.value}")

    simulated_annealing: LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver = LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver()
    simulated_annealing.solve_csp(board=board)

    pass


if __name__ == '__main__':
    main()
