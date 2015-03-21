import random
import math
import ea.config as config
from ea.crossover import OnePointCrossover
from ea.ea import EA
from ea.individual import AbstractFitnessEvaluator, AbstractIndividualFactory, Individual, \
    AbstractPhenotypeConvertor, BitToNumberPhenotypeConvertor
import matplotlib.pyplot as plt


class SurprisingFitnessEvaluator(AbstractFitnessEvaluator):
    def __init__(self, local):
        self.local = local

    def get_fitness(self, phenotype):
        if not self.check_phenotype_integrity(phenotype):
            return 0

        total_collisions = 0

        upper_range = 1 if self.local else len(phenotype) - 2
        for i in range(0, upper_range):
            total_collisions += self.is_surprising(phenotype, i)
        return 1/(1 + total_collisions)

    @staticmethod
    def is_surprising(seq, d):
        subseq = set()
        collisions = 0

        for i in range(0, len(seq)-d-1):
            word = (seq[i], seq[i+d+1])
            if word in subseq:
                collisions += 1
            else:
                subseq.add(word)

        return collisions

    @staticmethod
    def check_phenotype_integrity(phenotype):
        for num in phenotype:
            if num >= config.alphabet:
                return False
        return True


class SurprisingPhenotypeConvertor(BitToNumberPhenotypeConvertor):
    def __init__(self):
        super().__init__(0)
        self.cache = {}

    def __setstate__(self, dictd):
        self.cache = {}

    def get_length(self):
        return config.length


class SurprisingOnePointCrossover(OnePointCrossover):
    def split_point(self, a):
        pick = random.randint(0, config.length)
        return pick * int(len(a)/config.length)


class SurprisingIndividualFactory(AbstractIndividualFactory):
    def create(self, genotype=None):
        if genotype is None:
            genotype = []
            for i in range(0, config.length):
                genotype += self.to_binary(random.randint(0, config.alphabet-1), math.ceil(math.log2(config.alphabet)))

        return Individual(config.phenotype_convertor, config.fitness_evaluator, config.mutation_strategy, genotype,
                          config.crossover_strategy)

    @staticmethod
    def to_binary(num, length):
        binary = bin(num)[2:].zfill(length)
        return [int(digit) for digit in binary]


class SurprisingEA(EA):
    def __init__(self):
        self.intial_length = 3
        config.length = config.init_length
        super().__init__(config.individual_factory, config.adult_selector, config.parent_selector,
                         config.population_size, config.logging, config.plotting, config.generation_limit,
                         config.target_fitness)

    def run(self):
        length = config.init_length

        print("Starting SupSeq for alphabet:", config.alphabet)

        while True:
            print("Computing length:", length)
            self.compute()

            supr_seq = list(filter(lambda x: x.fitness() == 1, self.population.individuals))
            if len(supr_seq) > 0:
                print("Length", length, "found in generation", self.population.generation)
                print(supr_seq[0].phenotype())
            else:
                break

            length += 1
            setattr(config, 'length', length)
            self.population.initialize_population()

            plt.show()