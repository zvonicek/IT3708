import random
from ea.individual import AbstractFitnessEvaluator, AbstractPhenotypeConvertor, Individual, AbstractIndividualFactory
from ea.mutation import BinaryVectorInversionMutation
from ea_impl.suprising_sequences import SurprisingOnePointCrossover
from beer_tracker.beer_tracker_genotype import BeerTrackerGenotypeCoder


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
            coder.add_parameter(-5, 5, lambda: random.randint(-5, 5))

        # bias from interval [-10; 0]
        for i in range(0, self.ann.neurons_count()):
            coder.add_parameter(-10, 0, lambda: random.randint(-10, 0))

        # gains from interval [1,5]
        for i in range(0, self.ann.neurons_count()):
            coder.add_parameter(1, 5, lambda: random.randint(1, 5))

        # time constant from interval [1,2]
        for i in range(0, self.ann.neurons_count()):
            coder.add_parameter(1, 2, lambda: random.randint(1, 2))

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