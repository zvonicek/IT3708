class Neuron():
    def __init__(self, weights_count, activation_func):
        self.weights_count = weights_count
        self.weights = [0 for _ in range(weights_count)]
        self.activation_func = activation_func

    def compute(self, vals):
        sum = 0
        for i in range(0, len(vals)):
            sum += vals[i] * self.weights[i]
        return self.activation_func(sum)