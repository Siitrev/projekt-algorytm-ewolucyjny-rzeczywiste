import numpy as np
import numpy.random


def onePointCrossing(genome1 : str, genome2: str):

    random_point =  np.random.randint(1, len(genome1))
    tmp = genome1[random_point:]
    new_genome1 = genome1[:random_point] + genome2[random_point:]
    new_genome2 = genome2[:random_point] + tmp
    return new_genome1, new_genome2


def twoPointCrossing(genome1 : str, genome2: str):

    random_point = np.random.randint(0, len(genome1))
    random_point2 = np.random.randint(random_point+1, len(genome1)+1)

    new_genome1 = genome1[:random_point] + genome2[random_point:random_point2] + \
    genome1[random_point2:]

    new_genome2 = genome2[:random_point] + genome1[random_point:random_point2] + \
    genome2[random_point2:]

    return new_genome1, new_genome2
    

def homogeneousCrossing(genome1: str, genome2: str, probability_of_crossing : int):

    new_genome1 = ""
    new_genome2 = ""
    random_numbers = []

    for x in range(int(len(genome1)/2)):
        random_numbers.append(np.random.randint(0,100))
    
    random_numbers_counter = 0

    for x in range(len(genome1)):

        if x % 2 == 1:
            if random_numbers[random_numbers_counter] < probability_of_crossing:
                new_genome1 += genome2[x]
                new_genome2 += genome1[x]
                random_numbers_counter += 1
            else:
                new_genome1 += genome1[x]
                new_genome2 += genome2[x]
        if x % 2 == 0:
            new_genome1 += genome1[x]
            new_genome2 += genome2[x]

    return new_genome1, new_genome2


def heuristic_crossover(number1, number2):
    pot1 = []
    alfa = numpy.random.uniform(0, 1)
    if number1[0] <= number2[0] and number1[1] <= number2[1]:
        pot1[0] = number1[0] + alfa*(number1[1] - number1[0])
        pot1[1] = number2[0] + alfa*(number2[1] - number2[0])

    # tego nie bylo w pdf ale jest w ksiazce
    elif number1[0] >= number2[0] and number1[1] >= number2[1]:
        pot1[0] = number1[1] + alfa * (number1[0] - number1[1])
        pot1[1] = number2[1] + alfa * (number2[0] - number2[1])

    else:
        return number1  # ?????????? idk czy to dobry warunek ale idk co robic kiedy jest x1>x2 a y1<y2
    return pot1


def average_crossover(*args):
    n = len(args)
    pot = []
    sumx = 0
    sumy = 0

    for arg in args:
        sumx += arg[0]
        sumy += arg[1]

    pot[0] = sumx / n
    pot[1] = sumy / n

    return pot

