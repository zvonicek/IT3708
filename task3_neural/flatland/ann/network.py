class Network():
    def __init__(self, layers):
        self.layers = layers

    def compute(self, vals):
        for layer in self.layers:
            vals = layer.compute(vals)

        return vals

    def set_weights(self, weights):
        i = 0
        for layer in self.layers:
            for neuron in layer.neurons:
                for j in range(len(neuron.weights)):
                    neuron.weights[j] = weights[i]
                    i += 1