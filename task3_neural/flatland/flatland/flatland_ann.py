from ann.activation import StepActivation
from ann.ann import AbstractAnnFactory
from ann.layer import Layer
from ann.network import Network
from ann.neuron import Neuron


class FlatlandAnnFactory(AbstractAnnFactory):
    def create(self):

        activation_func = StepActivation()
        output_layer_f = Neuron(2, activation_func)
        output_layer_l = Neuron(2, activation_func)
        output_layer_r = Neuron(2, activation_func)

        output_layer = Layer([output_layer_f, output_layer_l, output_layer_r])

        network = Network([output_layer])

        return network