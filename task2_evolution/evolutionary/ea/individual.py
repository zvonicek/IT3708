import abc
import numpy
from ea.mutation import BinaryVectorInversionMutation


class AbstractIndividual(metaclass=abc.ABCMeta):
    def __init__(self, genotype, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator
        self.genotype = genotype

    def phenotype(self):
        return self.phenotype_convertor.get_phenotype(self)

    def fitness(self):
        return self.fitness_evaluator.get_fitness(self.phenotype())

    def mutate(self):
        self.genotype = self.mutation.mutate(self.genotype)


class Individual(AbstractIndividual):
    def __init__(self, phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, gene_length, crossover_strategy):
        self.mutation = mutation_strategy
        self.gene_length = gene_length
        self.crossover_strategy = crossover_strategy

        super().__init__(genotype, phenotype_convertor, fitness_evaluator)

    def __repr__(self):
        return ''.join(str(e) for e in self.genotype)


class AbstractPhenotypeConvertor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_phenotype(self, individual: 'Individual'):
        pass


class AbstractFitnessEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fitness(self, phenotype):
        pass


class AbstractIndividualFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, genotype=None):
        pass