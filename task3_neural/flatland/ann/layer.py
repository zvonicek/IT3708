class Layer():
    def __init__(self, neurons):
        self.neurons = neurons

    def compute(self, vals):
        res = []
        for neuron in self.neurons:
            res.append(neuron.compute(vals))

        return res

    def weights_count(self):
        return sum(x.weights_count for x in self.neurons)


class CtrnnLayer(Layer):
    def compute(self, vals):
        res = []
        # weight for self loops, ...
        layer_vals = [x.output for x in self.neurons]
        for neuron in self.neurons:
            res.append(neuron.compute(vals, layer_vals))

        return res

    def weights_count(self):
        return sum(x.weights_count + x.layer_neuron_num for x in self.neurons)