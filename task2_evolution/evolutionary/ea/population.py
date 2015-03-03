class Population:
    def __init__(self, individual_fact: 'IndividualFactory', population_size):
        self.individual_fact = individual_fact
        self.population_size = population_size

        self.individuals = self.generate(self.population_size)

    def generate(self, count):
        generated = []
        for i in range(0, count):
            generated.append(self.individual_fact.create())

        return generated