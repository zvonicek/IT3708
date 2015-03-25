from ann.activation import AbstractActivation


class Neuron():
    def __init__(self, weights_count, activation_func: AbstractActivation):
        self.weights_count = weights_count
        self.weights = [0 for _ in range(weights_count)]
        self.activation_func = activation_func

    def compute(self, vals):
        integration = self.integration(vals)
        return self.activation_func.get_output(integration)

    def integration(self, vals):
        integration_sum = 0
        for i in range(0, len(vals)):
            integration_sum += vals[i] * self.weights[i]
        return integration_sum