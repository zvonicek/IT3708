import abc
from math import exp


class AbstractActivation(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_output(self, value):
        pass


class StepActivation(AbstractActivation):
    def get_output(self, value):
        return value > 0


class SimpleActivation(AbstractActivation):
    def get_output(self, value):
        return value


class SigmoidActivation(AbstractActivation):
    def get_output(self, value):
        return 1 / (1 + exp(-value))


class TangentActivation(AbstractActivation):
    def get_output(self, value):
        return (exp(2*value) - 1) / (exp(2*value) + 1)