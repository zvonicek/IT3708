import abc
import random


class AbstractMutation(metaclass=abc.ABCMeta):
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    @abc.abstractmethod
    def mutate(self, genotype):
        pass


class BinaryVectorInversionMutation(AbstractMutation):
    def mutate(self, genotype):
        for i in range(0, len(genotype)):
            if random.random() < self.mutation_rate:
                genotype[i] = 1 if genotype[i] == 0 else 0
        return genotype