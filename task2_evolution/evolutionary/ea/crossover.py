import abc
import random


class AbstractCrossover(metaclass=abc.ABCMeta):
    def __init__(self, crossover_rate):
        self.crossover_rate = crossover_rate

    @abc.abstractmethod
    def crossover(self, a, b):
        pass


class OnePointCrossover(AbstractCrossover):
    def crossover(self, a, b):
        if random.random() < self.crossover_rate:
            split_point = self.split_point(a)
            return a[:split_point] + b[split_point:], b[:split_point] + a[split_point:]
        else:
            return a, b

    def split_point(self, a):
        return random.randint(1, len(a) - 1)