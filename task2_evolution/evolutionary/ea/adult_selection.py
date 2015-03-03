import abc
import heapq


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