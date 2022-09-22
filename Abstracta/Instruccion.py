from abc import ABC, abstractmethod
from Entorno.Entorno import Entorno


class Instruccion(ABC):
    def __init__(self, fila):
        super().__init__()
        self.fila = fila
        self.generador = None

    @abstractmethod
    def ejecutar(self, entorno: Entorno):
        pass
