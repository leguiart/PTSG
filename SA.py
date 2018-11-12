
import numpy as np
import math


class SimulatedAnnealing:
    """
    Clase para el algoritmo SimulatedAnnealing
    In:
    problema: es una clase que extiende de la clase LocalSearchProblem
    """
    def __init__(self, problema):
        self.problema = problema

    def search(self, c_enfriamiento,Tinit,Tend,n):
        """
        In:
        c_enfriamiento: constante de enfriamiento
        Tinit: Temperatura inicial
        Tend: Temperatura final
        n: número de movimientos a cada temperatura
        Out:
        donde x es la solución y v su energía
        """
        x = self.problema.aleatoria()
        v = self.problema.energia(x)
        T = Tinit
        while T > Tend:
            for i in range(n):
                xprima = self.problema.move(x.copy())
                vprima = self.problema.energia(xprima)
                if vprima < v:
                    x = xprima
                    v = vprima
                elif np.random.random_sample()<math.exp(-(vprima - v)/T):
                    x = xprima
                    v = vprima
            T = c_enfriamiento*T
        return (x,v)
