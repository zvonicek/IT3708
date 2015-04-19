import abc
from math import exp


class AbstractActivation(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_output(self, value):
        pass


class StepActivation(AbstractActivation):
    def get_output(self, value):
        return value > 0


class SigmoidActivation(AbstractActivation):
    def get_output(self, value):
        return 1 / (1 + exp(-value))