import abc
from functools import reduce
import heapq
import random


# adult selectors
class AbstractAdultSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select(self, population: 'Population'):
        pass


class FullGenerationalReplacementAdultSelector(AbstractAdultSelector):
    def select(self, population: 'Population'):
        population.individuals = population.generate(population.population_size)


class OverProductionAdultSelector(AbstractAdultSelector):
    def __init__(self, num_generated_children):
        self.num_generated_children = num_generated_children

    def select(self, population: 'Population'):
        offspring = population.generate(self.num_generated_children)
        population.individuals = heapq.nlargest(population.population_size, offspring, key=lambda x: x.fitness())


class GenerationalMixingAdultSelector(AbstractAdultSelector):
    def __init__(self, num_generated_children):
        self.num_generated_children = num_generated_children

    def select(self, population: 'Population'):
        pool = population.individuals
        pool += population.generate(self.num_generated_children)
        population.individuals = heapq.nlargest(population.population_size, pool, key=lambda x: x.fitness())


# parent selectors
class AbstractParentSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select_one(self, population: 'Population'):
        pass


class FitnessProportionateParentSelector(AbstractParentSelector):
    def select_one(self, population: 'Population'):
        max_val = sum(individual.fitness() for individual in population.individuals)
        pick = random.uniform(0, max_val)
        current = 0
        for individual in population.individuals:
            current += individual.fitness()
            if current > pick:
                return individual


class SigmaScalingParentSelector(AbstractParentSelector):
    def select_one(self, population: 'Population'):
        pass