from abc import ABC, abstractmethod
from Entorno.Entorno import Entorno


class Expresion(ABC):
    def __init__(self, fila):
        super().__init__()
        self.fila = fila
        self.generador = None
        self.isLabel = ""
        self.notLabel = ""

    @abstractmethod
    def ejecutar(self, entorno: Entorno):
        pass
