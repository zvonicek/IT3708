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
        self.compute()

        fittest = list(filter(lambda x: x.fitness() == 1, self.population.individuals))
        if len(fittest) > 0:
            # if logging is disabled, report the successful generation anyway
            if not config.logging:
                self.population.report()

            print("Found in generation", self.population.generation )
        else:
            print("Did not find within", self.population.generation , "generations")

        plt.show(block=True)

    def compute(self):
        if config.plotting:
            plt.clf()
            plt.axis([0, config.generation_limit, 0, 1])
            plt.ion()
            plt.show()

        while self.population.generation <= config.generation_limit and \
                not any(x for x in self.population.individuals if x.fitness() >= config.target_fitness):
            self.population.generation += 1

            self.population.select_adults()

            # mating
            self.population.mate()

            # mutation
            self.population.mutate()

            if config.plotting or config.logging:
                best = self.population.best_individual()
                avg, sd = self.population.avg_sd_fitness()

            if config.plotting:
                plt.scatter(self.population.generation, best.fitness(), c='r')
                plt.plot(self.population.generation, best.fitness(), c='r')
                plt.scatter(self.population.generation, avg, c='b')
                plt.scatter(self.population.generation, sd, c='g')
                plt.draw()
                print(end='')

            if config.logging:
                self.population.report(best, avg, sd)