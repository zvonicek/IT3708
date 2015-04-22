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

        for layer in self.layers:
            for neuron in layer.neurons:
                if neuron.bias:
                    # skaredy, pak prepsat, aby ty vahy byly ve vetsim rozsahu uz pri generovani
                    neuron.bias_weight = weights[i]*5
                    i += 1

        assert len(weights) == i, "some weights remains unassigned"

    def biased_neurons_count(self):
        biased_neurons = 0
        for layer in self.layers:
            for neuron in layer.neurons:
                if neuron.bias:
                    biased_neurons += 1

        return biased_neurons

    def weights_count(self):
        return sum(x.weights_count() for x in self.layers)

    def neurons_count(self):
        return sum(map(lambda x: len(x.neurons), self.layers))


class CtrnnNetwork(Network):
    def __init__(self, layers):
        super().__init__(layers)
        self.wraparound = True

    def set_weights(self, weights):
        i = 0

        for layer in self.layers:
            for neuron in layer.neurons:
                # weights among layers
                for j in range(len(neuron.weights)):
                    neuron.weights[j] = weights[i]
                    i += 1
                # weights inside layer
                for j in range(neuron.layer_neuron_num):
                    neuron.my_layer_weights[j] = weights[i]
                    i += 1

        for layer in self.layers:
            for neuron in layer.neurons:
                # set bias weight
                neuron.bias_weight = weights[i]
                i += 1

        for layer in self.layers:
            for neuron in layer.neurons:
                # set gain
                neuron.gain = weights[i]
                i += 1

        for layer in self.layers:
            for neuron in layer.neurons:
                # set time constant
                neuron.time_constant = weights[i]
                i += 1

        assert len(weights) == i, "some weights remains unassigned"