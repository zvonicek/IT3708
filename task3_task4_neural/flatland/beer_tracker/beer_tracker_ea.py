from collections import namedtuple
import sys
from beer_tracker.beer_tracker_ann import BeerTrackerAnnFactory

sys.path.append('../../task2_evolution/evolutionary')

import random
from tkinter import Tk
from ea.adult_selection import GenerationalMixingAdultSelector
from ea.ea import EA
from ea.individual import AbstractFitnessEvaluator, AbstractPhenotypeConvertor, Individual, AbstractIndividualFactory
from ea.mutation import BinaryVectorInversionMutation
from ea.parent_selection import SigmaScalingParentSelector
from beer_tracker.beer_tracker_genotype import BeerTrackerGenotypeCoder
from beer_tracker.gui import GUI
from beer_tracker.world import World
from flatland.flatland_ea import FlatlandOnePointCrossover


class BeerTrackerFitnessEvaluator(AbstractFitnessEvaluator):

    def __init__(self, world, ann):
        self.world = world
        self.ann = ann

    def get_fitness(self, phenotype):
        self.ann.set_weights(phenotype)

        return self.world.simulate(self.ann)


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
            if not self.ann.wraparound and i in [5, 6, 14, 15]:
                coder.add_parameter(-20, 20, lambda: random.uniform(-20, 20))
            else:
                coder.add_parameter(-5, 5, lambda: random.uniform(-0.5, 0.5))

        # bias from interval [-10; 0]
        for i in range(0, self.ann.neurons_count()):
            coder.add_parameter(-10, 0, lambda: random.uniform(-10, 0))

        # gains from interval [1,5]
        for i in range(0, self.ann.neurons_count()):
            coder.add_parameter(1, 5, lambda: random.uniform(1, 5))

        # time constant from interval [1,2]
        for i in range(0, self.ann.neurons_count()):
            coder.add_parameter(1, 2, lambda: random.uniform(1, 2))

        return coder

    def create(self, genotype=None):
        length = self.ann.weights_count() + self.ann.neurons_count()*3

        if genotype is None:
            genotype = self.genotype_coder.generate_init_genotype()

        phenotype_convertor = BeerTrackerPhenotypeConvertor(length, self.genotype_coder)
        fitness_evaluator = BeerTrackerFitnessEvaluator(self.world, self.ann)
        mutation_strategy = BinaryVectorInversionMutation(0.05)
        crossover_strategy = FlatlandOnePointCrossover(0.8, length)

        return Individual(phenotype_convertor, fitness_evaluator, mutation_strategy, genotype, crossover_strategy)


class BeerTrackerEA(EA):
    def __init__(self, pull_extension=False, wraparound=True):
        self.ann = BeerTrackerAnnFactory().create(pull_extension, wraparound)
        self.pull_extension = pull_extension

        self.params = namedtuple('Params', 'capture_reward avoidance_reward capture_punishment avoidance_punishment')
        self.world = World(self.fitness_parameters(), pull_extension, wraparound)

        individual_factory = BeerTrackerIndividualFactory(self.world, self.ann)
        adult_selector = GenerationalMixingAdultSelector()
        parent_selector = SigmaScalingParentSelector()
        population_size = 30

        if not wraparound:
            generation_limit = 50
        else:
            generation_limit = 40
        elitism_size = 5
        self.visualize_best = True
        super().__init__(individual_factory, adult_selector, parent_selector, population_size, True, False,
                         generation_limit, 100000.0, elitism_size)

    def fitness_parameters(self):
        capture_reward = 4
        avoidance_reward = 3
        capture_punishment = 3
        avoidance_punishment = 3.3

        return self.params(capture_reward, avoidance_reward, capture_punishment, avoidance_punishment)

    def compute(self):
        super().compute()

        best = self.population.best_individual()
        self.ann.set_weights(best.phenotype())

        if self.visualize_best:
            tk = Tk()
            gui = GUI(tk)
            gui.play(self.world, self.ann, (self.plot_max, self.plot_avg, self.plot_sd))
            tk.mainloop()


class BeerTrackerPullEA(BeerTrackerEA):
    def __init__(self):
        super().__init__(True, True)

    def fitness_parameters(self):
        capture_reward = 4.1
        avoidance_reward = 3.25
        capture_punishment = 3.1
        avoidance_punishment = 3.3

        return self.params(capture_reward, avoidance_reward, capture_punishment, avoidance_punishment)


class BeerTrackerNoWrapEA(BeerTrackerEA):
    def __init__(self):
        super().__init__(False, False)

    def fitness_parameters(self):
        capture_reward = 4.2
        avoidance_reward = 3
        capture_punishment = 3
        avoidance_punishment = 3.3

        return self.params(capture_reward, avoidance_reward, capture_punishment, avoidance_punishment)

