from ann.activation import StepActivation, SigmoidActivation, TangentActivation, SimpleActivation
from ann.ann import AbstractAnnFactory
from ann.layer import Layer
from ann.network import Network
from ann.neuron import Neuron


class FlatlandAnnFactory(AbstractAnnFactory):
    def create(self):

        activation_func_o = TangentActivation()
        activation_func_f = SimpleActivation()

        hidden_layer = []
        for _ in range(6):
            hidden_layer.append(Neuron(6, activation_func_o, True))

        output_layer = []
        for _ in range(3):
            output_layer.append(Neuron(6, activation_func_f))

        network = Network([Layer(hidden_layer), Layer(output_layer)])

        return network