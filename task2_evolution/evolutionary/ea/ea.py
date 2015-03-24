from ea.population import Population
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


class EA():
    def __init__(self, individual_fact: 'AbstractIndividualFactory', adult_selector: 'AbstractAdultSelector',
                 parent_selector: 'AbstractParentSelector', population_size, logging, plotting, generation_limit,
                 target_fitness):
        self.logging = logging
        self.plotting = plotting
        self.generation_limit = generation_limit
        self.target_fitness = target_fitness
        self.population = Population(individual_fact, population_size, parent_selector, adult_selector)

    def run(self):
        self.compute()

        fittest = list(filter(lambda x: x.fitness() == 1, self.population.individuals))
        if len(fittest) > 0:
            # if logging is disabled, report the successful generation anyway
            if not self.logging:
                best = self.population.best_individual()
                avg, sd = self.population.avg_sd_fitness()
                self.population.report(best, avg, sd)

            print("Found in generation", self.population.generation )
        else:
            print("Did not find within", self.population.generation , "generations")

        plt.show()

    def compute(self):
        plot_max = []
        plot_avg = []
        plot_sd = []

        while self.population.generation < self.generation_limit and \
                not any(x for x in self.population.individuals if x.fitness() >= self.target_fitness):
            self.population.generation += 1

            # mating
            self.population.mate()

            if self.plotting or self.logging:
                best = self.population.best_individual()
                avg, sd = self.population.avg_sd_fitness()

            if self.plotting:
                plot_max.append(best.fitness())
                plot_avg.append(avg)
                plot_sd.append(sd)

            if self.logging:
                self.population.report(best, avg, sd)

        if self.plotting:
            plt.plot(plot_max)
            plt.plot(plot_avg)
            plt.plot(plot_sd)
            prop = FontProperties()
            prop.set_size('small')
            plt.legend(['best', 'average', 'std'], loc='lower right', prop = prop)
            plt.ylim([0, 1])