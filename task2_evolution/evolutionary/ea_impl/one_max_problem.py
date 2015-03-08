from ea.individual import *
from ea.adult_selection import *
from ea.parent_selection import *
from ea.crossover import OnePointCrossover
from ea.ea import EA
from ea.individual import AbstractIndividualFactory, Individual
from ea.mutation import BinaryVectorInversionMutation


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
        gene_length = 40

        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(gene_length,)).tolist()

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, gene_length, crossover_strategy)


class OneMaxEA(EA):
    def __init__(self):
        individual_factory = OneMaxIndividualFactory()

        adult_selector = FullGenerationalReplacementAdultSelector()
        parent_selector = FitnessProportionateParentSelector()

        population_size = 170
        super().__init__(individual_factory, adult_selector, parent_selector, population_size)