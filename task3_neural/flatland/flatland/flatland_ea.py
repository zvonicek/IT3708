import random
import sys
from tkinter import Tk
from flatland.flatland import Cell, Turn, Flatland
from gui.gui import GUI

sys.path.append('../../task2_evolution/evolutionary')

from ea.adult_selection import GenerationalMixingAdultSelector
from ea.crossover import OnePointCrossover
from ea.ea import EA
from ea.parent_selection import SigmaScalingParentSelector
from ea.mutation import BinaryVectorInversionMutation
from ea.individual import AbstractIndividualFactory, AbstractFitnessEvaluator, Individual, AbstractPhenotypeConvertor


class FlatlandFitnessEvaluator(AbstractFitnessEvaluator):

    def __init__(self, flatlands, ann):
        self.flatlands = flatlands  # TODO property bude nutné při "dynamic" vždy znovu nastavovat
        self.ann = ann

    def get_fitness(self, phenotype):
        self.ann.set_weights(phenotype)

        fitness_sum = 0
        for flatland in self.flatlands:
            fitness_sum += flatland.simulate(self.ann)

        return fitness_sum / len(self.flatlands)


class SurprisingOnePointCrossover(OnePointCrossover):
    def __init__(self, crossover_rate, length):
        super().__init__(crossover_rate)
        self.length = length

    def split_point(self, a):
        pick = random.randint(0, self.length)
        return pick * int(len(a)/self.length)


class FlatlandPhenotypeConvertor(AbstractPhenotypeConvertor):
    """phenotype is a list of weights – values from interval [-1; 1]"""

    def __init__(self, length):
        """length is a count of distinct numbers encoded in genotype"""
        self.length = length

    def get_phenotype(self, genotype):
        chunk = int(len(genotype)/self.length)

        numbers = []
        for number in zip(*[iter(genotype)]*chunk):
            number_dec = int(''.join(map(str, number)), 2)
            # scale number to desired interval [-1; 1]
            numbers += [2 * number_dec / (2**chunk - 1) - 1]

        return numbers


class FlatlandIndividualFactory(AbstractIndividualFactory):
    def __init__(self, flatland, ann):
        self.bits_per_weight = 8
        self.flatland = flatland
        self.ann = ann

    def create(self, genotype=None):
        length = self.ann.weights_count()

        if genotype is None:
            # lecture06-slide21: it is recommended to initialize weights from interval [-0,1; 0,1]
            vals = [x for x in range(2**self.bits_per_weight) if abs(2*x/(2**self.bits_per_weight)-1) <= 0.1]
            genotype = []
            for i in range(0, length):
                genotype += self.to_binary(random.choice(vals), self.bits_per_weight)

        phenotype_convertor = FlatlandPhenotypeConvertor(length)
        fitness_evaluator = FlatlandFitnessEvaluator(self.flatland, self.ann)
        mutation_strategy = BinaryVectorInversionMutation(0.01)
        crossover_strategy = SurprisingOnePointCrossover(0.8, length)

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, crossover_strategy)

    @staticmethod
    def to_binary(num, length):
        binary = bin(num)[2:].zfill(length)
        return [int(digit) for digit in binary]


class FlatlandEA(EA):
    def __init__(self, ann, dynamic=False, scenarios=1):
        # neural network for solving problem
        self.ann = ann
        self.dynamic = dynamic
        self.scenarios = scenarios

        # initialize flatlands
        self.flatlands = self.generate_flatlands()

        individual_factory = FlatlandIndividualFactory(self.flatlands, self.ann)
        adult_selector = GenerationalMixingAdultSelector()
        parent_selector = SigmaScalingParentSelector()
        population_size = 30
        generation_limit = 40
        elitism_size = 5
        self.visualize_best = True
        super().__init__(individual_factory, adult_selector, parent_selector, population_size, True, False,
                         generation_limit, 1.0, elitism_size)

    def generate_flatlands(self):
        flatlands = []
        for i in range(self.scenarios):
            flatlands.append(Flatland(10, (1/3, 1/3), (2, 2)))

        return flatlands

    def compute(self):
        super().compute()

        best = self.population.best_individual()
        self.ann.set_weights(best.phenotype())

        if self.visualize_best:
            tk = Tk()
            gui = GUI(tk)
            gui.replay_scenarios(self.flatlands, self.ann)
            tk.mainloop()

    def compute_generation(self):
        super().compute_generation()

        # in dynamic mode generate new worlds on each new generation
        if self.dynamic:
            self.flatlands[0:len(self.flatlands)] = self.generate_flatlands()