import random

from board import Board
import numpy as np
import copy
import random

B : Board = Board()
#grid = B.grid
#print(grid)
print_grid = np.zeros([9, 9])

def population(board: Board):
    pop = []
    # generate population
    popsize: int = 25
    #temp_board = board
    for i in range(popsize):
        temp_board = Board()
        #temp_board = board
        #temp_board = copy.copy(board)
        # print("org", board.__str__())
        # print("copy", temp_board.__str__())
        #temp_grid = np.copy(board.grid)
        for row in range(9):
            for col in range(9):
                if temp_board.grid[row][col].value == 0:
                    random_number = random.randint(1, 9)
                    temp_board.grid[row][col].value = random_number
        pop.insert(i, temp_board)
                #print_grid[row][col] = grid[row][col].value
                # if temp_grid[row][col].value == 0:
                #     random_number = random.randint(1, 9)
                #     temp_grid[row][col].value = random_number
                #     #print_grid[row][col] = random_number
                #     pop.insert(i, temp_grid)
    #print(print_grid)
    print(len(pop))
    for i in pop:
        print('start', i.__str__())



population(B)