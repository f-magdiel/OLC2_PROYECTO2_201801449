from abc import ABC, abstractmethod
from Generador.Generador import Generador
from Entorno.Entorno import Entorno


class Instruccion(ABC):
    def __init__(self):
        super().__init__()
        self.generador = Generador()

    @abstractmethod
    def ejecutar(self, entorno: Entorno):
        pass
