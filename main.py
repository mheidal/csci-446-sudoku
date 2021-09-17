from board import Board
from cell import Cell
from local_search_simulated_annealing_minimum_conflict_constraint_solver import \
    LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver


def main():
    board: Board = Board()
    print(f"board.value:\t{board.value}")
    easy_p1_sol: Board = Board(board_file_name="Easy-P1-sol")
    print(f"sol.value:\t{easy_p1_sol.value}")
    print(easy_p1_sol)  # TODO: if iterations is complete pass the current board back into the solver...

    simulated_annealing: LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver = LocalSearchSimulatedAnnealingMinimumConflictConstraintSolver()
    solved: bool = simulated_annealing.solve_csp(board=board)
    if solved is False:
        for row in simulated_annealing.solutions[0].grid:
            for cell in row:
                sol_cell: Cell = easy_p1_sol.grid[cell.get_row_index()][cell.get_col_index()]
                if cell.value != sol_cell.value:
                    print(cell)
    pass


if __name__ == '__main__':
    main()
