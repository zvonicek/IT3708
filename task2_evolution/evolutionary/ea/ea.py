from functools import reduce
from ea.population import Population
import matplotlib.pyplot as plt
import ea.config as config


class EA():
    def __init__(self, individual_fact: 'AbstractIndividualFactory', adult_selector: 'AbstractAdultSelector',
                 parent_selector: 'AbstractParentSelector', population_size):
        self.individual_fact = individual_fact
        self.adult_selector = adult_selector
        self.population = Population(individual_fact, population_size, parent_selector, adult_selector)

    def run(self):
        generation = self.compute()

        for ind in self.population.individuals:
            print(ind.phenotype(), ind.fitness())

        print(generation)

        plt.show(block=True)

    def compute(self):
        plt.axis([0, config.generation_limit, 0, 1])
        plt.ion()
        plt.show()

        generation = 0
        while generation <= config.generation_limit and \
                not any(x for x in self.population.individuals if x.fitness() >= config.target_fitness):
            generation += 1

            self.population.select_adults()

            # mating
            self.population.mate()

            # mutation
            self.population.mutate()

            plt.scatter(generation, max(self.population.individuals, key=lambda x: x.fitness()).fitness(), c='r')
            fitnesses = list(map(lambda x: x.fitness(), self.population.individuals))
            plt.scatter(generation, sum(fitnesses) / len(fitnesses), c='b')
            plt.draw()
            print(end='')

        plt.clf()
        return generation