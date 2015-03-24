import abc
import heapq


class AbstractAdultSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select(self, population, select_count):
        pass


class FullGenerationalReplacementAdultSelector(AbstractAdultSelector):
    def select(self, population, select_count):
        return population.children


class OverProductionAdultSelector(AbstractAdultSelector):
    def select(self, population, select_count):
        return heapq.nlargest(select_count, population.children, key=lambda x: x.fitness())


class GenerationalMixingAdultSelector(AbstractAdultSelector):
    def select(self, population, select_count):
        pool = population.individuals
        pool += population.children
        return heapq.nlargest(select_count, pool, key=lambda x: x.fitness())