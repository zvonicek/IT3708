import numpy
from ea.adult_selection import *
from ea.crossover import OnePointCrossover
from ea.ea import EA
from ea.individual import AbstractFitnessEvaluator, BasicPhenotypeConvertor, AbstractIndividualFactory, Individual
from ea.mutation import BinaryVectorInversionMutation
from ea.parent_selection import *


class LOLZFitnessEvaluator(AbstractFitnessEvaluator):
    def __init__(self, z):
        self.z = z

    def get_fitness(self, phenotype):
        count = 0
        target_value = None
        for bit in phenotype:
            if count == 0:
                target_value = bit

            if bit == target_value and (bit == 1 or (bit == 0 and count < self.z)):
                count += 1
            else:
                break

        return count/len(phenotype)


class LOLZIndividualFactory(AbstractIndividualFactory):
    def create(self, genotype=None):
        phenotype_convertor = BasicPhenotypeConvertor()
        fitness_evaluator = LOLZFitnessEvaluator(21)
        mutation_strategy = BinaryVectorInversionMutation(0.1)
        crossover_strategy = OnePointCrossover(0.9)
        gene_length = 40

        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(gene_length,)).tolist()

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, gene_length, crossover_strategy)


class LOLZEA(EA):
    def __init__(self):
        individual_factory = LOLZIndividualFactory()

        adult_selector = GenerationalMixingAdultSelector()
        #parent_selector = SigmaScalingParentSelector()
        parent_selector = TournamentParentSelector(5, 0.5)

        population_size = 20
        super().__init__(individual_factory, adult_selector, parent_selector, population_size)