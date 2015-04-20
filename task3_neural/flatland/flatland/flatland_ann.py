from ann.activation import StepActivation, SigmoidActivation, TangentActivation, SimpleActivation
from ann.ann import AbstractAnnFactory
from ann.layer import Layer
from ann.network import Network
from ann.neuron import Neuron


class FlatlandAnnFactory(AbstractAnnFactory):
    def create(self):

        activation_func_o = TangentActivation()
        activation_func_f = SimpleActivation()

        output_layer = []
        for _ in range(6):
            output_layer.append(Neuron(6, activation_func_o, True))

        final_layer = []
        for _ in range(3):
            final_layer.append(Neuron(3, activation_func_f))

        network = Network([Layer(output_layer), Layer(final_layer)])

        return network