from ea.individual import *
from ea.ea import EA
from ea.individual import AbstractIndividualFactory, Individual
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
        gene_length = config.gene_length

        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(gene_length,)).tolist()

        return Individual(config.phenotype_convertor, config.fitness_evaluator, config.mutation_strategy, genotype,
                          config.crossover_strategy)


class OneMaxEA(EA):
    def __init__(self):
        super().__init__(config.individual_factory, config.adult_selector, config.parent_selector,
                         config.population_size, config.logging, config.plotting, config.generation_limit,
                         config.target_fitness)
