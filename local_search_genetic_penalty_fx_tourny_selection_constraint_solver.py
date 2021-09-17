import random

from board import Board
import numpy as np
import copy
import random

B : Board = Board()

def population(board: Board) -> list:
    pop = []
    popsize: int = 25
    for i in range(popsize):
        temp_board = copy.deepcopy(board)
        for row in range(9):
            for col in range(9):
                if temp_board.grid[row][col].value == 0:
                    random_number = random.randint(1, 9)
                    temp_board.grid[row][col].value = random_number
        pop.insert(i, temp_board)

    return pop

def fitness(pop: list):
    fit_dict = {}
    fit_prob_list = []
    total_fit = 0
    for i in pop:
        total_fit += (1/i.value)
    for i in pop:
        fit_dict[i] = i.value
        #fit_prob_list.append((i.value/total_fit) * 100)
    # print(fit_dict)
    # print(fit_prob_list)
    return fit_dict
   #tournamnet_selection(fit_prob_list, pop, fit_dict)

#def tournamnet_selection(fit_prob_list: list, pop: list, fit_dict: dict):
def tournamnet_selection(fit_dict: dict):
    pop = list(fit_dict.keys())
    fit_list = list(fit_dict.values())
    total_fit = sum(fit_list)
    fit_prob_list = []
    for i in range(len(fit_list)):
        fit_prob_list.insert(i, ((1/fit_list[i])/total_fit) * 100)
    combatant = random.choices(pop, weights=fit_prob_list, k=1)[0]
    gladiator = random.choices(pop, weights=fit_prob_list, k=1)[0]
    # while loop that makes sure combatant and gladiator are differant boards
    while(combatant.value == gladiator.value):
        gladiator = random.choices(pop, weights=fit_prob_list, k=1)[0]
    if gladiator.value > combatant.value:
        return gladiator
    else:
        return combatant

def crossover(mom: Board, dad: Board) -> Board:
    child_1: Board = Board()
    child_2: Board = Board()
    #crossover point
    random_row = random.randint(0,8)
    random_col = random.randint(0,8)

    for row in range(9):
        for col in range(9):
            if (row <= random_row and col <= random_col):
                mom[row][col].value = child_1[row][col].value
                dad[row][col].value = child_2[row][col].value
            else:
                mom[row][col].value = child_1[row][col].value
                dad[row][col].value = child_2[row][col].value
    # print(mom.__str__())
    # dad.__str__()
    # child_1.__str__()
    # child_2.__str__()



pop_val = []
pop = population(B)
for i in range(len(pop)):
    pop_val.insert(i, pop[i].value)

# while(min(pop_val) != 0):
#     fit_dict = fitness(pop)
#     dad = tournamnet_selection(fit_dict)
#     mom = tournamnet_selection(fit_dict)
#     while(dad.value == mom.value):
#         mom = tournamnet_selection(fit_dict)
#     child = crossover(dad, mom)

fit_dict = fitness(pop)
dad = tournamnet_selection(fit_dict)
mom = tournamnet_selection(fit_dict)
while(dad.value == mom.value):
    mom = tournamnet_selection(fit_dict)
child = crossover(dad, mom)
