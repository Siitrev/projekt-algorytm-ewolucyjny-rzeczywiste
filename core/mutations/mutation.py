import numpy as np
from core.template.template import Chromosome

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

