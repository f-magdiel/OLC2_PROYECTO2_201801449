from abc import ABC, abstractmethod
from Entorno.Entorno import Entorno


class Expresion(ABC):
    def __init__(self):
        super().__init__()
        #self.generador: Generador = None
        self.isLabel = ""
        self.notLabel = ""

    @abstractmethod
    def ejecutar(self, entorno: Entorno):
        pass
