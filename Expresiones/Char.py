from Abstracta.Expresion import Expresion
from Entorno.Entorno import Entorno
from Entorno.Valor import Valor
from Enum.TipoPrimitivo import TipoPrimitivo


class Char(Expresion):
    def __init__(self, fila, tipo, valor):
        super().__init__(fila)
        self.fila = fila
        self.tipo = tipo
        self.valor = valor

    def ejecutar(self, entorno: Entorno):
        return Valor(self.fila, str(ord(self.valor)), False, TipoPrimitivo.CHAR)
