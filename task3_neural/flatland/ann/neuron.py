from ann.activation import AbstractActivation


class Neuron():
    def __init__(self, weights_count, activation_func: AbstractActivation, bias=False):
        self.weights_count = weights_count
        self.weights = [0 for _ in range(weights_count)]
        self.activation_func = activation_func
        self.bias = bias
        if bias:
            self.bias_weight = 0

    def compute(self, vals):
        integration = self.integration(vals)

        return self.activation_func.get_output(integration)

    def integration(self, vals):
        integration_sum = 0
        for val, weight in zip(vals, self.weights):
            integration_sum += val * weight

        if self.bias:
            integration_sum += self.bias_weight
        return integration_sum


class CtrnnNeuron(Neuron):
    def __init__(self, weights_count, activation_func: AbstractActivation, time_constant, layer_neuron_num):
        super(CtrnnNeuron, self).__init__(weights_count, activation_func)
        self.state = 0
        self.gain = 0
        self.time_constant = time_constant
        self.layer_neuron_num = layer_neuron_num
        self.my_layer_weights = [0 for _ in range(layer_neuron_num)]
        self.bias_weight = 0
        self.time_constant = time_constant
        self.output = 0

    def integration(self, vals, my_layer_vals=[]):
        result = super(CtrnnNeuron, self).integration(vals)
        result += self.bias_weight
        for val, weight in zip(my_layer_vals, self.my_layer_weights):
            result += val * weight
        return result

    def compute(self, vals, my_layer_vals=[]):
        integration = self.integration(vals, my_layer_vals)
        derivation = (1/self.time_constant)*(-self.state + integration)
        self.state += derivation

        self.output = self.activation_func.get_output(self.state*self.gain)
        return self.output