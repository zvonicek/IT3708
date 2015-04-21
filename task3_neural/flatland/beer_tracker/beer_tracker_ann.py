from ann.activation import SigmoidActivation
from ann.ann import AbstractAnnFactory
from ann.layer import Layer, CtrnnLayer
from ann.network import Network, CtrnnNetwork
from ann.neuron import CtrnnNeuron


class BeerTrackerAnnFactory(AbstractAnnFactory):
    def create(self, pull_extension=False):
        activation_func = SigmoidActivation()
        hidden_layer = []
        output_layer = []

        for i in range(2):
            # time constant: [1,2]
            hidden_layer.append(CtrnnNeuron(5, activation_func, 1, 2))

        if pull_extension:
            num_output_neurons = 3
        else:
            num_output_neurons = 2
        for i in range(num_output_neurons):
            # time constant: [1,2]
            output_layer.append(CtrnnNeuron(2, activation_func, 1, 2))

        network = CtrnnNetwork([CtrnnLayer(hidden_layer), CtrnnLayer(output_layer)])

        return network