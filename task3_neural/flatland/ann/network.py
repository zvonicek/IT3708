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

    def weights_count(self):
        return sum(x.weights_count() for x in self.layers)

    def neurons_count(self):
        return sum(map(lambda x: len(x.neurons), self.layers))


class CtrnnNetwork(Network):

    # Ty neurony je treba prochazet tak blbe nekolikrat, protoze chci zachovat poradi tech vah v poli (napr. bias ma jiny rozsah nez gain)
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
