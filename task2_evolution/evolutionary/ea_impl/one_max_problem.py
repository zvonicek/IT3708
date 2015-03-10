from ea.individual import *
from ea.adult_selection import *
from ea.parent_selection import *
from ea.crossover import OnePointCrossover
from ea.ea import EA
from ea.individual import AbstractIndividualFactory, Individual
from ea.mutation import BinaryVectorInversionMutation
import ea.config as config

class OneMaxFitnessEvaluator(AbstractFitnessEvaluator):
    def get_fitness(self, phenotype):
        ones = 0
        for bit in phenotype:
            if bit == 1:
                ones += 1
        return ones/len(phenotype)


class OneMaxIndividualFactory(AbstractIndividualFactory):
    def create(self, genotype=None):
        phenotype_convertor = BasicPhenotypeConvertor()
        fitness_evaluator = OneMaxFitnessEvaluator()
        mutation_strategy = BinaryVectorInversionMutation(0.001)
        crossover_strategy = OnePointCrossover(0.9)
        gene_length = config.gene_length

        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(gene_length,)).tolist()

        return Individual(config.phenotype_convertor, config.fitness_evaluator, config.mutation_strategy, genotype,
                          config.crossover_strategy)


class OneMaxEA(EA):
    def __init__(self):
        individual_factory = OneMaxIndividualFactory()

        adult_selector = FullGenerationalReplacementAdultSelector()
        parent_selector = FitnessProportionateParentSelector()

        population_size = 170
        super().__init__(config.individual_factory, config.adult_selector, config.parent_selector, config.population_size)
