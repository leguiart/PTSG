from abc import ABCMeta, abstractmethod
class LocalSearchProblem:
    """
    aleatoria: genera solución aleatoria
    energía: calcula la energía del argumento x
    move: transforma x en una solución vecina x'
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def aleatoria(self):
        pass

    @abstractmethod
    def energia(self,x):
        pass

    @abstractmethod
    def move(self,x):
        pass

    @abstractmethod
    def energiaPromedio(self, x):
        pass
