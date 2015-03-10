import numpy


class Population:
    def __init__(self, individual_fact: 'IndividualFactory', population_size, parent_selector, adult_selector):
        self.individual_fact = individual_fact
        self.population_size = population_size
        self.parent_selector = parent_selector
        self.adult_selector = adult_selector
        self.children = []
        self.individuals = []
        self.generation = 0

        self.initialize_population()

    def initialize_population(self):
        self.children = self.generate(self.population_size)
        self.individuals = []
        self.generation = 0

    def generate(self, count):
        generated = []
        for i in range(0, count):
            generated.append(self.individual_fact.create())

        return generated

    def mate(self):
            new_generation = []
            while len(new_generation) < self.population_size:
                first, second = self.crossover()

                new_generation.append(first)
                new_generation.append(second)

            self.children = new_generation

    def crossover(self):
        parent_1 = self.parent_selector.select_one(self)
        parent_2 = self.parent_selector.select_one(self)

        genotype_1, genotype_2 = parent_1.crossover_strategy.crossover(parent_1.genotype, parent_2.genotype)
        return self.individual_fact.create(genotype_1), self.individual_fact.create(genotype_2)

    def mutate(self):
        for individual in self.individuals:
            individual.mutate()

    def select_adults(self):
        self.individuals = self.adult_selector.select(self)
        self.children = []

    # reporting functions
    def report(self, best, avg, sd):
        print("generation:", self.generation, "best-f:", best.fitness(), "avg-f:", avg, "sd-f:", sd,
              "best-ph:", best.phenotype_string())

    def best_individual(self):
        return max(self.individuals, key=lambda x: x.fitness())

    def avg_sd_fitness(self):
        fitnesses = list(map(lambda x: x.fitness(), self.individuals))
        return numpy.mean(fitnesses), numpy.std(fitnesses)