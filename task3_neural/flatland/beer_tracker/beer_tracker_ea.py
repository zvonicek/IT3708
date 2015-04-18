import random
from ea.individual import AbstractFitnessEvaluator, AbstractPhenotypeConvertor, Individual, AbstractIndividualFactory
from ea.mutation import BinaryVectorInversionMutation
from ea_impl.suprising_sequences import SurprisingOnePointCrossover


class BeerTrackerFitnessEvaluator(AbstractFitnessEvaluator):

    def __init__(self, worlds, ann):
        self.worlds = worlds
        self.ann = ann

    def get_fitness(self, phenotype):
        self.ann.set_weights(phenotype)
        fitness_sum = 0

        for world in self.worlds:
            fitness_sum += world.simulate(self.ann)

        return fitness_sum / len(self.worlds)


class BeerTrackerPhenotypeConvertor(AbstractPhenotypeConvertor):
    def __init__(self, length, genotype_coder):
        """length is a count of distinct numbers encoded in genotype"""
        self.length = length
        self.genotype_coder = genotype_coder

    def get_phenotype(self, genotype):
        chunk = int(len(genotype)/self.length)

        numbers_dec = []

        for number in zip(*[iter(genotype)]*chunk):
            numbers_dec.append(int(''.join(map(str, number)), 2))

        return self.genotype_coder.decode_genotype(numbers_dec)


class BeerTrackerGenotypeCoder():
    """ Holds the configuration of the genotype parameters and provides a way to encode/decode genotype"""
    def __init__(self, bits_per_weight):
        self.min_ranges = []
        self.max_ranges = []
        self.init_funcs = []
        self.bits_per_weight = bits_per_weight

    def add_parameter(self, min_range, max_range, init_func):
        """
        Add new genotype parameter
        :param min_range: minimum range (eg. -1)
        :param max_range: maximum range (eg. +1)
        """

        self.min_ranges.append(min_range)
        self.max_ranges.append(max_range)
        self.init_funcs.append(init_func)

    def generate_init_genotype(self):
        genotype = []
        for i in range(len(self.init_funcs)):
            encoded_value = self.encode_decimal_value(self.init_funcs[i](), self.min_ranges[i], self.max_ranges[i])
            genotype.extend(self.to_binary(encoded_value, self.bits_per_weight))

        return genotype

    def decode_genotype(self, genotype):
        assert len(genotype) == len(self.min_ranges), "wrong input length"

        output = []
        for i in range(len(genotype)):
            output.append(self.decode_decimal_value(genotype[i], self.min_ranges[i], self.max_ranges[i]))

        return output

    def decode_decimal_value(self, value, min_range, max_range):
        """ Decodes the value from decimal genotype
        :param value: decimal value to be decoded (eg. 120)
        :param min_range: minimum range (eg. -1)
        :param max_range: maximum range (eg. +1)
        :return: decimal output value (eg. -0.01)
        """

        return (max_range - min_range) * value/(2**self.bits_per_weight-1) + min_range

    def encode_decimal_value(self, value, min_range, max_range):
        """ Encodes decimal value to decimal genotype representation, output is the closest possible value from the interval
        :param value: decimal input value (eg. -0.01)
        :param min_range: minimum range (eg. -1)
        :param max_range: maximum range (eg. +1)
        :return: decoded output to interval [0, 2^self.bits_number_per_weight] in decimal (eg. 120)
        """

        return min(range(2**self.bits_per_weight),
                   key=lambda x: abs(self.decode_decimal_value(x, min_range, max_range)-value))

    @staticmethod
    def to_binary(num, length):
        binary = bin(num)[2:].zfill(length)
        return [int(digit) for digit in binary]


class BeerTrackerIndividualFactory(AbstractIndividualFactory):
    def __init__(self, world, ann):
        self.bits_per_weight = 8
        self.world = world
        self.ann = ann
        self.genotype_coder = self.initialize_genotype_coder()

    def initialize_genotype_coder(self):
        # the genotype contains:
        # weights of the synapis ([-5,+5])
        # bias weight for every neuron in ann (bias and input neurons are not modeled explicitly in our ann) ([-10,0])
        # gains for every neuron ([1,5])
        # time constant for every neuron ([1,2])

        coder = BeerTrackerGenotypeCoder(self.bits_per_weight)

        # weights from interval [-5; 5]
        for i in range(0, self.ann.weights_count()):
            self.genotype_coder.add_parameter(-5, 5, lambda: random.randint(-5, 5))

        # bias from interval [-10; 0]
        for i in range(0, self.ann.neurons_count()):
            self.genotype_coder.add_parameter(-10, 0, lambda: random.randint(-10, 0))

        # gains from interval [1,5]
        for i in range(0, self.ann.neurons_count()):
            self.genotype_coder.add_parameter(1, 5, lambda: random.randint(1, 5))

        # time constant from interval [1,2]
        for i in range(0, self.ann.neurons_count()):
            self.genotype_coder.add_parameter(1, 2, lambda: random.randint(1, 2))

        return coder

    def create(self, genotype=None):
        length = self.ann.weights_count() + self.ann.neurons_count()*3

        if genotype is None:
            genotype = self.genotype_coder.generate_init_genotype()

        phenotype_convertor = BeerTrackerPhenotypeConvertor(length)
        fitness_evaluator = BeerTrackerFitnessEvaluator(self.flatland, self.ann)
        mutation_strategy = BinaryVectorInversionMutation(0.01)
        crossover_strategy = SurprisingOnePointCrossover(0.8, length)

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, crossover_strategy)

#TODO BeerTrackerEA, kde pojede ten samotny EA