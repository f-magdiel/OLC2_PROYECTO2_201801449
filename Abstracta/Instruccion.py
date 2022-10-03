from abc import ABC, abstractmethod


class Instruccion(ABC):
    def __init__(self, fila):
        super().__init__()
        self.fila = fila

    @abstractmethod
    def convertir(self, generador, entorno):
        pass
