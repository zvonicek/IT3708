import abc
import heapq


class AbstractAdultSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select(self, population):
        pass


class FullGenerationalReplacementAdultSelector(AbstractAdultSelector):
    def select(self, population):
        return population.children


class OverProductionAdultSelector(AbstractAdultSelector):
    def select(self, population):
        return heapq.nlargest(population.population_size, population.children, key=lambda x: x.fitness())


class GenerationalMixingAdultSelector(AbstractAdultSelector):
    def select(self, population):
        pool = population.individuals
        pool += population.children
        return heapq.nlargest(population.population_size, pool, key=lambda x: x.fitness())