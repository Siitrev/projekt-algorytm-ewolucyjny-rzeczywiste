import numpy as np
import numpy.random
import benchmark_functions as bf

# def heuristic_crossover(number1, number2):
#     pot1 = []
#     alfa = numpy.random.uniform(0, 1)
#     if number1[0] <= number2[0] and number1[1] <= number2[1]:
#         pot1[0] = number1[0] + alfa*(number1[1] - number1[0])
#         pot1[1] = number2[0] + alfa*(number2[1] - number2[0])

#     # tego nie bylo w pdf ale jest w ksiazce
#     elif number1[0] >= number2[0] and number1[1] >= number2[1]:
#         pot1[0] = number1[1] + alfa * (number1[0] - number1[1])
#         pot1[1] = number2[1] + alfa * (number2[0] - number2[1])

#     else:
#         return number1  # ?????????? idk czy to dobry warunek ale idk co robic kiedy jest x1>x2 a y1<y2
#     return pot1

def heuristic_crossover(number1, number2, maximalization=True):
    pot = []
    fitness_1 = bf.Michalewicz(*number1)
    fitness_2 = bf.Michalewicz(*number2)
    alfa = numpy.random.uniform(0, 1)
    if maximalization and fitness_2 > fitness_1:
        pot[0] = number1[0] + alfa*(number1[1] - number1[0])
        pot[1] = number2[0] + alfa*(number2[1] - number2[0])

    # tego nie bylo w pdf ale jest w ksiazce
    elif not maximalization and fitness_2 < fitness_1:
        pot[0] = number1[1] + alfa * (number1[0] - number1[1])
        pot[1] = number2[1] + alfa * (number2[0] - number2[1])

    else:
        return None  # ?????????? idk czy to dobry warunek ale idk co robic kiedy jest x1>x2 a y1<y2
    return pot


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

