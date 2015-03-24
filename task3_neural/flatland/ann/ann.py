import abc


class AbstractAnnFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self):
        pass