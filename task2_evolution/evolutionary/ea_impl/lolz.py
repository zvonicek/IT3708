import numpy
from ea.ea import EA
from ea.individual import AbstractFitnessEvaluator, BasicPhenotypeConvertor, AbstractIndividualFactory, Individual
import ea.config as config


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
        gene_length = config.gene_length

        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(gene_length,)).tolist()

        return Individual(config.phenotype_convertor, config.fitness_evaluator, config.mutation_strategy, genotype,
                          config.crossover_strategy)


class LOLZEA(EA):
    def __init__(self):
        super().__init__(config.individual_factory, config.adult_selector, config.parent_selector, config.population_size)