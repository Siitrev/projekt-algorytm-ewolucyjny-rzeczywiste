import numpy as np
import numpy.random
import random
import benchmark_functions as bf

def check_range(number1, number2, downLimit : float, upperLimit : float, **kwargs):

    if (number1[0] > downLimit and number1[1] > downLimit):
        if (number2[0] > downLimit and number2[1] > downLimit):
            if (number1[0] < upperLimit and number1[1] < upperLimit):
                if (number2[0] < upperLimit and number2[1] < upperLimit):
                    return True
    return False

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

def heuristic_crossover(number1, number2, downLimit : float, upperLimit : float, maximalization=True, **kwargs):
    pot = []
    fitness = bf.Michalewicz()
    fitness_1 = fitness(number1)
    fitness_2 = fitness(number2)
    alfa = numpy.random.uniform(0, 1)
    if maximalization and fitness_2 > fitness_1:
        pot.append(number1[0] + alfa*(number1[1] - number1[0]))
        pot.append(number2[0] + alfa*(number2[1] - number2[0]))

    # tego nie bylo w pdf ale jest w ksiazce
    elif not maximalization and fitness_2 < fitness_1:
        pot.append(number1[0] + alfa*(number1[1] - number1[0]))
        pot.append(number2[0] + alfa*(number2[1] - number2[0]))

    else:
        return None  # ?????????? idk czy to dobry warunek ale idk co robic kiedy jest x1>x2 a y1<y2
    return pot


def average_crossover(number1, number2, downLimit : float, upperLimit : float, **kwargs):
    pot = []
    sumx = number1[0] + number2[0]
    sumy = number1[1] + number2[1]

    pot.append(sumx / 2)
    pot.append(sumy / 2)

    return pot

def arithmetic_crossing(number1, number2, downLimit : float, upperLimit : float, **kwargs):

    while (1):
        k = 0
        while(k == 0):
            k = random.random()
        
        newNumber1 = []
        newNumber2 = []

        newNumber1.append(k * number1[0] + (1 - k) * number2[0])
        newNumber1.append(k * number1[1] + (1 - k) * number2[1])
        newNumber2.append((1 - k) * number1[0] + k * number2[0])
        newNumber2.append((1 - k) * number1[1] + k * number2[1])

        if (check_range(newNumber1, newNumber2, downLimit, upperLimit)):
            break
    
    return newNumber1, newNumber2

def flat_crossing(number1, number2, downLimit : float, upperLimit : float, **kwargs):

    while (1):
        newNumber1 = []
        newNumber2 = []
        
        newNumber1.append(random.uniform(number1[0], number2[0]))
        newNumber1.append(random.uniform(number1[1], number2[1]))
        newNumber2.append(random.uniform(number1[0], number2[0]))
        newNumber2.append(random.uniform(number1[1], number2[1]))
        
        if (check_range(newNumber1, newNumber2, downLimit, upperLimit)):
            break
    
    return newNumber1, newNumber2