import numpy as np
from typing import Callable
import benchmark_functions as bf
from copy import deepcopy 


class Person:
    def __init__(self, chromosome_x: np.float64, chromosome_y: np.float64) -> None:
        self.fitness_function = bf.Michalewicz()
        self.chromosomes = [chromosome_x, chromosome_y]
        self.value = self.fitness_function(self.chromosomes)

    def upadte_value(self):
        self.value = self.fitness_function(self.chromosomes)
    
    def __str__(self) -> str:
        return str(
            tuple(self.chromosomes)
            + (self.value,)
        )

    def __repr__(self) -> str:
        return str(self)



class Population:
    def __init__(self, size: int, start: np.float64, end: np.float64) -> None:
        self.people = [Person((end - start) * np.random.rand() + start, (end - start) * np.random.rand() + start) for _ in range(size)]

    def add_people(self, people):
        for person in people:
            self.people.append(person)

    def remove_people(self, amount=1):
        for _ in range(amount):
            index = np.random.randint(0, len(self.people))
            self.people.pop(index)

    def __repr__(self) -> str:
        temp = [
            tuple(
                person.chromosomes
                + [person.value]
            )
            for person in self.people
        ]
        return str(temp).replace("),", ")\n") + "-----------------------------------------------------------------\n"


class Experiment:
    def __init__(self, size: int, start: np.float64, end: np.float64) -> None:
        self.population = Population(size, start, end)
        self.best_people = []

    def mutate(self, mutation: Callable, probability: float = 0.3, points : int = 1):
        
        for person in self.population.people:
            chance = np.random.rand()
            
            if chance <= probability:
                mutation(person.chromosomes, points)

    def cross(self, crossing: Callable,  probability : float = 0.8, **kwargs):
        population_len = len(self.population.people)
        target_population = population_len - len(self.best_people)
        crossing_len = len(self.people_for_crossing)
        counter = 0
        
        while counter < target_population:
            chance = np.random.rand()
            index_1 = np.random.randint(0, crossing_len)
            index_2 = np.random.randint(0, crossing_len)
            
            if chance <= probability:
                chromosomes_1 = self.people_for_crossing[index_1].chromosomes

                chromosomes_2 = self.people_for_crossing[index_2].chromosomes
                
                crossing(chromosomes_1, chromosomes_2)
                
                self.population.people[counter].upadte_value()
                counter += 1
                
                self.population.people[counter].upadte_value()
                counter += 1
        self.population.people = self.population.people[:target_population]

    def selection(
        self,
        select_method: Callable,
        amount: float,
        maximization: bool = False,
        **kwargs
    ):
        if "contestants" in kwargs:
            self.people_for_crossing = select_method(
                self.population,
                amount=amount,
                maximization=maximization,
                number_of_contestants=kwargs["contestants"],
            )
        else:
            self.people_for_crossing = select_method(
                self.population, amount=amount, maximization=maximization
            )

    def save_best_people(self, amount: int = 1, maximization: bool = False):
        self.best_people = []
        temp = sorted(self.population.people, reverse=maximization, key=lambda x: x.value)
        for person in temp[:amount]:
            copy_person = deepcopy(person)
            self.best_people.append(copy_person)

    def get_result(self, maximization: bool = False) -> Person:
        if maximization:
            return max(self.population.people, key=lambda person: person.value)
        return min(self.population.people, key=lambda person: person.value)
    
    def get_db_data(self, maximization : bool) -> tuple:
        data = [person.value for person in self.population.people]
        std = np.std(data)
        avg = np.average(data)
        if maximization:
            best = np.max(data)
        else:
            best = np.min(data)
        return (best,avg,std)

