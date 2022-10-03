from abc import ABC, abstractmethod


class Expresion(ABC):
    def __init__(self, fila):
        super().__init__()
        self.fila = fila
        self.generador = None

    @abstractmethod
    def convertir(self, entorno):
        pass
