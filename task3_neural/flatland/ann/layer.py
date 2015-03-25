class Layer():
    def __init__(self, neurons):
        self.neurons = neurons

    def compute(self, vals):
        res = []
        for neuron in self.neurons:
            res.append(neuron.compute(vals[:neuron.weights_count]))
            vals = vals[neuron.weights_count:]

        return res

    def weights_count(self):
        return sum(x.weights_count for x in self.neurons)