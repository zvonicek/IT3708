class Layer():
    def __init__(self, neurons):
        self.neurons = neurons

    def compute(self, vals):
        res = []
        for neuron in self.neurons:
            res.append(neuron.compute(vals[:neuron.weights_count]))
            vals = vals[neuron.weights_count:]

        return res