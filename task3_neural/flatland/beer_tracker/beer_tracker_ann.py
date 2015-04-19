from ann.activation import SigmoidActivation
from ann.ann import AbstractAnnFactory
from ann.layer import Layer, CtrnnLayer
from ann.network import Network
from ann.neuron import CtrnnNeuron


class BeerTrackerAnnFactory(AbstractAnnFactory):
    def create(self):
        activation_func = SigmoidActivation()
        hidden_layer = []
        output_layer = []

        for i in range(2):
            # time constant: [1,2]
            hidden_layer.append(CtrnnNeuron(5, activation_func, 1, 2))

        for i in range(2):
            # time constant: [1,2]
            output_layer.append(CtrnnNeuron(2, activation_func, 1, 2))

        network = Network([CtrnnLayer(hidden_layer), CtrnnLayer(output_layer)])

        return network