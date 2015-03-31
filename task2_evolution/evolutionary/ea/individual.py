import abc


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
        self._phenotype = self.phenotype_convertor.get_phenotype(attribute)
        self._fitness = self.fitness_evaluator.get_fitness(self.phenotype())

    def phenotype(self):
        return self._phenotype

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
        return self.phenotype_string()

    def phenotype_string(self):
        return ', '.join(str(e) for e in self.phenotype())


class AbstractPhenotypeConvertor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_phenotype(self, genotype):
        pass


class BasicPhenotypeConvertor(AbstractPhenotypeConvertor):
    def get_phenotype(self, genotype):
        return genotype


class BitToNumberPhenotypeConvertor(AbstractPhenotypeConvertor):
    def __init__(self, length):
        self.length = length
        self.cache = {}

    def get_phenotype(self, genotype):
        chunk = int(len(genotype)/self.get_length())

        numbers = []
        for number in zip(*[iter(genotype)]*chunk):
            if number not in self.cache:
                self.cache[number] = [int(''.join(map(str, number)), 2)]
            numbers += self.cache[number]

        return numbers

    def get_length(self):
        return self.length


class AbstractFitnessEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fitness(self, phenotype):
        pass


class AbstractIndividualFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, genotype=None):
        pass