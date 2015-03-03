from ea.population import Population
from ea.crossover import OnePointCrossover


class EA():
    def __init__(self, individual_fact: 'AbstractIndividualFactory', adult_selector: 'AbstractAdultSelector',
                 parent_selector: 'AbstractParentSelector', crossover_strategy: 'AbstractCrossover', population_size):
        self.crossover_strategy = crossover_strategy
        self.individual_fact = individual_fact
        self.adult_selector = adult_selector
        self.parent_selector = parent_selector
        self.population = Population(individual_fact, population_size)

    def run(self, generation_limit, fitness_threshold):
        generation = 0
        while generation <= generation_limit and not any(x for x in self.population.individuals if x.fitness() >= fitness_threshold):
            # adult selection
            self.adult_selector.select(self.population)

            # mating
            new_generation = []
            while len(new_generation) < self.population.population_size:
                first, second = self.crossover()

                new_generation.append(first)
                new_generation.append(second)

            self.population.individuals = new_generation

            # mutation
            self.mutate()

            for i in self.population.individuals:
                print(i.fitness(), " ", end='')
            print()
            generation += 1

    def crossover(self):
        parent_1 = self.parent_selector.select_one(self.population)
        parent_2 = self.parent_selector.select_one(self.population)

        #print("before crossover: ", parent_1.genotype, parent_2.genotype)
        genotype_1, genotype_2 = self.crossover_strategy.crossover(parent_1.genotype, parent_2.genotype)
        #print("after crossover: ", genotype_1, genotype_2)
        return self.individual_fact.create(genotype_1), self.individual_fact.create(genotype_2)

    def mutate(self):
        for individual in self.population.individuals:
            individual.mutate()
