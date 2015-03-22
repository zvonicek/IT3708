import random
import sys
from ea.crossover import OnePointCrossover

sys.path.append('../../task2_evolution/evolutionary')

from ea.mutation import BinaryVectorInversionMutation
from ea.individual import AbstractIndividualFactory, AbstractFitnessEvaluator, Individual


class FlatlandFitnessEvaluator(AbstractFitnessEvaluator):
    def get_fitness(self, phenotype):
        #TODO fitness function
        pass


class SurprisingOnePointCrossover(OnePointCrossover):
    def __init__(self, crossover_rate, length):
        super().__init__(crossover_rate)
        self.length = length

    def split_point(self, a):
        pick = random.randint(0, self.length)
        return pick * int(len(a)/self.length)


class FlatlandIndividualFactory(AbstractIndividualFactory):
    def create(self, genotype=None):
        #TODO generate new genotype if not given

        #TODO length should be
        length = None

        #TODO genotype -> phenotype convertor
        phenotype_convertor = None
        fitness_evaluator = FlatlandFitnessEvaluator()
        mutation_strategy = BinaryVectorInversionMutation(0.01)
        crossover_strategy = SurprisingOnePointCrossover(0.8, len(genotype))

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, crossover_strategy)