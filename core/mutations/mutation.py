import numpy as np
from core.template.template import Chromosome


def mutation(old_chromosome: Chromosome, points: int) -> str:
    genome = old_chromosome.get()  # bo get zwraca self.genome ?
    length = len(genome)
    inverted = list(genome)  # bo na stringu sie nie da

    # Losowanie indeksu bitu
    index = np.random.randint(0, length)
    inverted[index] = "0" if genome[index] == "1" else "1"

    if points == 2:
        index2 = np.random.randint(0, length)
        while index2 == index:
            index2 = np.random.randint(0, length)
        inverted[index2] = "0" if genome[index2] == "1" else "1"

    # new_chromosome = inverted
    new_chromosome = "".join(inverted)
    return new_chromosome


"""
def mutation(old_chromosome, points):
    genome = old_chromosome.get  # bo get zwraca self.genome ?
    length = len(genome)

    inverted = list(genome)  # bo na stringu sie nie da

    i = 1
    while i <= points:  # czyli 1 <= 1 lub 1 <= 2
        i += 1
        index = random.randint(0, length)
        inverted[index] = '0' if genome[index] == '1' else '1'

    new_chromosome = "".join(inverted)
    return new_chromosome

"""
