class Layer():
    def __init__(self, neurons):
        self.neurons = neurons

    def compute(self, vals):
        res = []
        for neuron in range(self.neurons):
            res.append(neuron.compute(vals))

        return res