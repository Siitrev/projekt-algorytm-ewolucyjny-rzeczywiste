import numpy as np
import random

def mutation_Gauss(ind, start, end):
    avg = 0
    sigma = 1  # ustawić dowolne odchylenie standardowe
    def_ind0 = ind[0]
    def_ind1 = ind[1]
    while True:
        number = np.random.normal(avg, sigma)

        ind[0] = ind[0] + number
        ind[1] = ind[1] + number

        if ind[0] < end and ind[0] > start and ind[1] > start and ind[1] < end:
            break; 
        
        ind[0] = def_ind0
        ind[1] = def_ind1

def uniform_mutation(number1, downLimit, upperLimit):
  
    randomMutation = random.randint(0, 1) 
    newNumber1[randomMutation] = random.uniform(downLimit, upperLimit)
        
    return newNumber1

def mutation_index_flip(number1):
    return [number1[1], number1[0]]
