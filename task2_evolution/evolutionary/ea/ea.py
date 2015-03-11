from functools import reduce
from ea.population import Population
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import ea.config as config


class EA():
    def __init__(self, individual_fact: 'AbstractIndividualFactory', adult_selector: 'AbstractAdultSelector',
                 parent_selector: 'AbstractParentSelector', population_size):
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

        plt.show()

    def compute(self):
        if config.plotting:
            plot_max = []
            plot_avg = []
            plot_sd = []

        while self.population.generation < config.generation_limit and \
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
                plot_max.append(best.fitness())
                plot_avg.append(avg)
                plot_sd.append(sd)

            if config.logging:
                self.population.report(best, avg, sd)

        if config.plotting:
            plt.plot(plot_max)
            plt.plot(plot_avg)
            plt.plot(plot_sd)
            prop = FontProperties()
            prop.set_size('small')
            plt.legend(['best', 'average', 'std'], loc='lower right', prop = prop)
            plt.ylim([0, 1])