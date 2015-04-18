import random
from individual import AbstractFitnessEvaluator, AbstractPhenotypeConvertor, Individual, AbstractIndividualFactory
from mutation import BinaryVectorInversionMutation
from suprising_sequences import SurprisingOnePointCrossover


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
    def __init__(self, length):
        """length is a count of distinct numbers encoded in genotype"""
        self.length = length

    def get_phenotype(self, genotype):
        chunk = int(len(genotype)/self.length)

        numbers = []
        # TODO
        """for number in zip(*[iter(genotype)]*chunk):
            number_dec = int(''.join(map(str, number)), 2)
            # scale number to desired interval [-1; 1]
            numbers += [2 * number_dec / (2**chunk - 1) - 1]
        """
        return numbers


class BeerTrackerIndividualFactory(AbstractIndividualFactory):
    def __init__(self, world, ann):
        self.bits_per_weight = 8
        self.world = world
        self.ann = ann

    def create(self, genotype=None):
        # the genotype contains:
        # weights of the synapis ([-5,+5])
        # bias weight for every neuron in ann (bias and input neurons are not modeled explicitly in our ann) ([-10,0])
        # gains for every neuron ([1,5])
        # time constant for every neuron ([1,2])

        length = self.ann.weights_count() + self.ann.neurons_count()*3

        if genotype is None:
            genotype = []

            # weights from interval [-5; 5]
            for i in range(0, self.ann.weights_count()):
                genotype += self.to_binary(random.randint(-5, 5), self.bits_per_weight)

            # bias from interval [-10; 0]
            for i in range(0, self.ann.neurons_count()):
                genotype += self.to_binary(random.randint(-10, 0), self.bits_per_weight)

            # gains from interval [1,5]
            for i in range(0, self.ann.neurons_count()):
                genotype += self.to_binary(random.randint(1, 5), self.bits_per_weight)

            # time constant from interval [1,2]
            for i in range(0, self.ann.neurons_count()):
                genotype += self.to_binary(random.randint(1, 2), self.bits_per_weight)

        phenotype_convertor = BeerTrackerPhenotypeConvertor(length)
        fitness_evaluator = BeerTrackerFitnessEvaluator(self.flatland, self.ann)
        mutation_strategy = BinaryVectorInversionMutation(0.01)
        crossover_strategy = SurprisingOnePointCrossover(0.8, length)

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, crossover_strategy)

    @staticmethod
    def to_binary(num, length):
        binary = bin(num)[2:].zfill(length)
        return [int(digit) for digit in binary]

#TODO BeerTrackerEA, kde pojede ten samotny EA