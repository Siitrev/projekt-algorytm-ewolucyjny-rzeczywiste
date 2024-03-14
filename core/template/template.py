import numpy as np
from typing import Callable
import benchmark_functions as bf
from copy import deepcopy 

class ChromosomeInfo:
    def __init__(self, start: np.float64, end: np.float64, precision: np.uint64) -> None:
        self.start = start
        self.end = end
        self.precision = precision


class Chromosome:
    def __init__(self, chromosome_info: ChromosomeInfo) -> None:
        self.__end = np.float64(chromosome_info.end)
        self.__start = np.float64(chromosome_info.start)
        self.__precision = np.uint64(chromosome_info.precision)
        self.m = np.ceil(
            np.log2((self.__end - self.__start) * np.power(10, self.__precision))
            + np.log2(1)
        )
        self.m = np.int64(self.m)
        self.randoms = [np.random.randint(0, 2) for _ in range(int(self.m))]
        self.genome = "".join([str(bit) for bit in self.randoms])

    def to_number(self) -> float:
        addent = (
            int(self.genome, 2)
            * (self.__end - self.__start)
            / (np.power(2, self.m) - 1)
        )
        return self.__start + addent

    def set(self, chromosome: str):
        self.genome = chromosome

    def get(self) -> str:
        return self.genome

    def __str__(self) -> str:
        return self.genome


class Person:
    def __init__(self, chromosome_info: ChromosomeInfo) -> None:
        self.fitness_function = bf.Michalewicz()
        self.chromosomes = (Chromosome(chromosome_info), Chromosome(chromosome_info))
        first_chromosome = self.chromosomes[0].to_number()
        second_chromosome = self.chromosomes[1].to_number()
        self.value = self.fitness_function([first_chromosome, second_chromosome])

    def upadte_value(self):
        first_chromosome = self.chromosomes[0].to_number()
        second_chromosome = self.chromosomes[1].to_number()
        self.value = self.fitness_function([first_chromosome, second_chromosome])
    
    def __str__(self) -> str:
        return str(
            tuple([chromosome.to_number() for chromosome in self.chromosomes])
            + (self.value,)
        )

    def __repr__(self) -> str:
        return str(self)



class Population:
    def __init__(self, size: int, chromosome_info: ChromosomeInfo) -> None:
        self.people = [Person(chromosome_info) for _ in range(size)]

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
                [chromosome.to_number() for chromosome in person.chromosomes]
                + [person.value]
            )
            for person in self.people
        ]
        return str(temp).replace("),", ")\n") + "-----------------------------------------------------------------\n"


class Experiment:
    def __init__(self, size: int, chromosome_info: ChromosomeInfo) -> None:
        self.population = Population(size, chromosome_info)
        self.chromosome_info = chromosome_info
        self.best_people = []

    def mutate(self, mutation: Callable, probability: float = 0.3, points : int = 1):
        
        for index, person in enumerate(self.population.people):
            chance = np.random.rand()
            
            if chance <= probability:
                new_chromosome_1 = mutation(person.chromosomes[0], points)
                new_chromosome_2 = mutation(person.chromosomes[1], points)

                self.population.people[index].chromosomes[0].set(new_chromosome_1)
                self.population.people[index].chromosomes[0].set(new_chromosome_2)

    def inverse(self, inversion: Callable, probability: float = 0.1):
        for index, person in enumerate(self.population.people):
            chance = np.random.rand()

            if chance <= probability:
                new_chromosome_1 = inversion(person.chromosomes[0].get())
                new_chromosome_2 = inversion(person.chromosomes[1].get())

                self.population.people[index].chromosomes[0].set(new_chromosome_1)
                self.population.people[index].chromosomes[0].set(new_chromosome_2)

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
                chromosome_1_x = self.people_for_crossing[index_1].chromosomes[0].get()
                chromosome_1_y = self.people_for_crossing[index_1].chromosomes[1].get()

                chromosome_2_x = self.people_for_crossing[index_2].chromosomes[0].get()
                chromosome_2_y = self.people_for_crossing[index_2].chromosomes[1].get()
                
                if "homogeneous" in kwargs:
                    new_chromosomes_x = crossing(chromosome_1_x, chromosome_2_x, probability)
                    new_chromosomes_y = crossing(chromosome_1_y, chromosome_2_y, probability)
                else:
                    new_chromosomes_x = crossing(chromosome_1_x, chromosome_2_x)
                    new_chromosomes_y = crossing(chromosome_1_y, chromosome_2_y)
                
                self.population.people[counter].chromosomes[0].set(new_chromosomes_x[0])
                self.population.people[counter].chromosomes[0].set(new_chromosomes_y[0])
                self.population.people[counter].upadte_value()
                counter += 1
                
                self.population.people[counter].chromosomes[1].set(new_chromosomes_x[1])
                self.population.people[counter].chromosomes[1].set(new_chromosomes_y[1])
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

