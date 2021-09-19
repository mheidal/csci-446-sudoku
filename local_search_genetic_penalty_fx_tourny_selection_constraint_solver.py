import random

from board import Board
import numpy as np
import copy
import random

B : Board = Board()
popsize: int = 30

def random_board(board: Board):
    temp_board = copy.deepcopy(board)
    for row in range(9):
        for col in range(9):
            if temp_board.grid[row][col].value == 0:
                random_number = random.randint(1, 9)
                temp_board.grid[row][col].value = random_number
    return temp_board

def population(board: Board) -> list:
    pop = []
    for i in range(popsize):
        #temp_board = random_board(board)
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
    #print(fit_dict)
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
        fit_prob_list.insert(i, ((1/fit_list[i])/total_fit) * 1000000)
    #print("fit_prop_list",fit_prob_list)
    #print("fit_list", fit_list)
    combatant = random.choices(pop, weights=fit_prob_list, k=1)[0]
    gladiator = random.choices(pop, weights=fit_prob_list, k=1)[0]

    # print("Combatant", combatant.value, "gladiator", gladiator.value)
    # while loop that makes sure combatant and gladiator are differant boards
    while combatant.value == gladiator.value:
        gladiator = random.choices(pop, weights=fit_prob_list, k=1)[0]
    if gladiator.value < combatant.value:
        return gladiator
    else:
        return combatant
    #return combatant

def crossover(dad: Board, mom: Board) -> Board:
    child_1: Board = Board()
    child_2: Board = Board()
    #crossover point
    random_row = random.randint(0,8)
    random_col = random.randint(0,8)

    for row in range(9):
        for col in range(9):
            if row <= random_row and col <= random_col:
                child_1[row][col].value = mom[row][col].value
                child_2[row][col].value = dad[row][col].value
            else:
                child_2[row][col].value = mom[row][col].value
                child_1[row][col].value = dad[row][col].value
    # print("Mom",mom.__str__())
    # print("Dad",dad.__str__())
    # print("Child 1", child_1.__str__())
    # print("Child 2",child_2.__str__())
    return [child_1, child_2]

def mutate(children: list):
    mutation_rate = 1/81
    child_1 = children[0]
    child_2 = children[1]
    # print("before")
    # print(child_1.__str__())
    # print(child_2.__str__())
    for row in range(9):
        for col in range(9):
            if random.random() < mutation_rate:
                if not child_1[row][col].preset:
                    child_1[row][col].value = random.randint(1,9)
    for row in range(9):
        for col in range(9):
            if random.random() < mutation_rate:
                if not child_1[row][col].preset:
                    child_2[row][col].value = random.randint(1,9)
    # print("after")
    # print(child_1.__str__())
    # print(child_2.__str__())
    return [child_1, child_2]




def replace(pop_val: list):
    new_pop = []
    while len(new_pop) < int(popsize * 0.8):
        dad = tournamnet_selection(fit_dict)
        mom = tournamnet_selection(fit_dict)
        while (dad.value == mom.value):
            mom = tournamnet_selection(fit_dict)
        children = crossover(dad, mom)
        children = mutate(children)
        new_pop.append(children[0])
        new_pop.append(children[1])
    n = popsize - len(new_pop)
    for i in range(n):
        rand_int = random.randint(0, len(pop) - 1)
        #print(pop_val.index(min(pop_val)))
        #print("1",pop_val)
        # new_pop.append(pop[pop_val.index(min(pop_val))])
        # del pop_val[pop_val.index(min(pop_val))]
        # del pop[0]
        #print("2",pop_val)
        new_pop.append(pop[rand_int])
        #new_pop.append(random_board(B))
    return new_pop

def update_pop_val(pop: list):
    pop_val = []
    for i in range(len(pop)):
        pop_val.insert(i, pop[i].value)
    return pop_val


gen = 0
pop = population(B)
pop_val = update_pop_val(pop)

while(min(pop_val) != 0):
    fit_dict = fitness(pop)
    pop = replace(pop_val)
    pop_val = update_pop_val(pop)
    #print(min(pop_val))
    gen = gen + 1
    #print("gen", gen)
print("done")
print(pop[pop_val.index(0)].__str__(), gen)

# while(min(pop_val) != 0):
#     fit_dict = fitness(pop)
#     dad = tournamnet_selection(fit_dict)
#     mom = tournamnet_selection(fit_dict)
#     while(dad.value == mom.value):
#         mom = tournamnet_selection(fit_dict)
#     child = crossover(dad, mom)

# fit_dict = fitness(pop)
# dad = tournamnet_selection(fit_dict)
# mom = tournamnet_selection(fit_dict)
# # print("Mom",mom.__str__())
# # print("Dad",dad.__str__())
# while(dad.value == mom.value):
#     mom = tournamnet_selection(fit_dict)
# children = crossover(dad, mom)
# children = mutate(children)
# #pop = replace()




