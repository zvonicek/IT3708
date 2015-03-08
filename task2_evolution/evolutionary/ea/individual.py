import abc
import numpy
from ea.mutation import BinaryVectorInversionMutation


class AbstractIndividual(metaclass=abc.ABCMeta):
    def __init__(self, genotype, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator
        self.genotype = genotype

    @property
    def genotype(self):
        return self._genotype

    @genotype.setter
    def genotype(self, attribute):
        self._genotype = attribute
        self._fitness = self.fitness_evaluator.get_fitness(self.phenotype())

    def phenotype(self):
        return self.phenotype_convertor.get_phenotype(self)

    def fitness(self):
        return self._fitness

    def mutate(self):
        self.genotype = self.mutation.mutate(self.genotype)


class Individual(AbstractIndividual):
    def __init__(self, phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, crossover_strategy):
        self.mutation = mutation_strategy
        self.crossover_strategy = crossover_strategy

        super().__init__(genotype, phenotype_convertor, fitness_evaluator)

    def __repr__(self):
        return ''.join(str(e) for e in self.genotype)


class AbstractPhenotypeConvertor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_phenotype(self, individual: 'Individual'):
        pass


class BasicPhenotypeConvertor(AbstractPhenotypeConvertor):
    def get_phenotype(self, ind: 'Individual'):
        return ind.genotype


class AbstractFitnessEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fitness(self, phenotype):
        pass


class AbstractIndividualFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, genotype=None):
        pass