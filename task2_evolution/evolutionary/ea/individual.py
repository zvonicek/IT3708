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
    def __init__(self, phenotype_convertor, fitness_evaluator, mutation_rate, genotype=None):
        if genotype is None:
            genotype = numpy.random.choice([0, 1], size=(self.gene_length,))

        self.mutation = BinaryVectorInversionMutation(mutation_rate)
        super().__init__(genotype, phenotype_convertor, fitness_evaluator)

    @property
    def gene_length(self):
        return 5

    @staticmethod
    def crossover(self, a, b):
        pass


class AbstractPhenotypeConvertor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_phenotype(self, individual: 'Individual'):
        pass


class AbstractFitnessEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fitness(self, phenotype):
        pass


class IndividualFactory():
    def __init__(self, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator', mutation_rate):
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator
        self.mutation_rate = mutation_rate

    def create_random(self):
        return Individual(self.phenotype_convertor, self.fitness_evaluator, self.mutation_rate)

    def create(self, genotype):
        return Individual(self.phenotype_convertor, self.fitness_evaluator, self.mutation_rate, genotype=genotype)