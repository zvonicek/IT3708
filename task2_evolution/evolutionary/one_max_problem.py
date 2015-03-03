import numpy
from ea import individual
from ea.adult_selection import *
from ea.crossover import OnePointCrossover
from ea.ea import EA
from ea.individual import AbstractIndividualFactory, Individual
from ea.mutation import BinaryVectorInversionMutation
from ea.parent_selection import FitnessProportionateParentSelector


class OneMaxPhenotypeConvertor(individual.AbstractPhenotypeConvertor):
    def get_phenotype(self, ind: 'Individual'):
        return ind.genotype


class OneMaxFitnessEvaluator(individual.AbstractFitnessEvaluator):
    def get_fitness(self, phenotype):
        ones = 0
        for bit in phenotype:
            if bit == 1:
                ones += 1
        return ones/len(phenotype)


class OneMaxIndividualFactory(AbstractIndividualFactory):
    def create(self, genotype=None):
        phenotype_convertor = OneMaxPhenotypeConvertor()
        fitness_evaluator = OneMaxFitnessEvaluator()
        mutation_strategy = BinaryVectorInversionMutation(0.1)
        gene_length = 20

        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(gene_length,)).tolist()

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, gene_length)


class OneMaxEA(EA):
    def __init__(self):
        individual_factory = OneMaxIndividualFactory()

        adult_selector = GenerationalMixingAdultSelector(30)
        parent_selector = FitnessProportionateParentSelector()
        crossover_strategy = OnePointCrossover(0.8)
        population_size = 20
        super().__init__(individual_factory, adult_selector, parent_selector, crossover_strategy, population_size)