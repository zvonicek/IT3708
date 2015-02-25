import abc
import numpy


class Population:
    def __init__(self, phenotype_convertor: 'AbstractPhenotypeConvertor', fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator
        self.population_size = 5

        self.individuals = self.generate(self.population_size)

    def generate(self, count):
        generated = []
        for i in range(0, count):
            generated.append(Individual(self.phenotype_convertor, self.fitness_evaluator))

        return generated


class Individual:
    def __init__(self, phenotype_convertor: 'AbstractPhenotypeConvertor', fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.genotype = numpy.random.choice([0, 1], size=(self.gene_length,))
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator

    @property
    def gene_length(self):
        return 5

    def phenotype(self):
        return self.phenotype_convertor.get_phenotype(self)

    def fitness(self):
        return self.fitness_evaluator.get_fitness(self.phenotype())


class AbstractPhenotypeConvertor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_phenotype(self, individual: 'Individual'):
        pass


class AbstractFitnessEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fitness(self, phenotype):
        pass