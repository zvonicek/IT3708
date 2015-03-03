import abc
import numpy


class AbstractIndividual(metaclass=abc.ABCMeta):
    def __init__(self, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator

    @abc.abstractmethod
    def phenotype(self):
        pass

    @abc.abstractmethod
    def fitness(self):
        pass


class Individual(AbstractIndividual):
    def __init__(self, genotype, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.genotype = genotype
        super().__init__(phenotype_convertor, fitness_evaluator)

    def __init__(self, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.genotype = numpy.random.choice([0, 1], size=(self.gene_length,))
        super().__init__(phenotype_convertor, fitness_evaluator)

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


class IndividualFactory():
    def __init__(self, phenotype_convertor: 'AbstractPhenotypeConvertor',
                 fitness_evaluator: 'AbstractFitnessEvaluator'):
        self.phenotype_convertor = phenotype_convertor
        self.fitness_evaluator = fitness_evaluator

    def create_random(self):
        return Individual(self.phenotype_convertor, self.fitness_evaluator)

    def create(self, genotype):
        return Individual(genotype, self.phenotype_convertor, self.fitness_evaluator)