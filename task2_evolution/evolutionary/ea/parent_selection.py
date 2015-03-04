import abc
from operator import methodcaller
import random
import math
from numpy import std, mean


class AbstractParentSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select_one(self, population: 'Population'):
        pass


class FitnessProportionateParentSelector(AbstractParentSelector):
    def select_one(self, population: 'Population'):
        fitnesses = list(map(lambda x: x.fitness(), population.individuals))

        exp_vals = self.exp_vals(fitnesses)
        pick = random.uniform(0, len(fitnesses))
        current = 0
        for val in exp_vals:
            current += val
            if current > pick:
                return population.individuals[exp_vals.index(val)]

    def exp_vals(self, fitnesses):
        m = mean(fitnesses)
        return list(map(lambda x: x/m, fitnesses))


class SigmaScalingParentSelector(FitnessProportionateParentSelector):
    def exp_vals(self, fitnesses):
        return list(map(lambda x: 1 + (x - mean(fitnesses))/(2*std(fitnesses)), fitnesses))


class BoltzmannParentSelector(FitnessProportionateParentSelector):
    def __init__(self, t):
        self.t = t

    def exp_vals(self, fitnesses):
        x = [math.exp(x / self.t) for x in fitnesses]
        return [nom/mean(x) for nom in x]


class TournamentParentSelector(AbstractParentSelector):
    def __init__(self, group_size, epsilon):
        self.group_size = group_size
        self.epsilon = epsilon

    def select_one(self, population: 'Population'):
        pick = random.sample(population.individuals, self.group_size)

        if random.uniform(0, 1) > self.epsilon:
            return max(pick, key=methodcaller('fitness'))
        else:
            return random.choice(pick)