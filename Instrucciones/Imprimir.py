from Abstracta.Instruccion import Instruccion
from Entorno.Entorno import Entorno
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Imprimir(Instruccion):
    def __init__(self, fila, expresion):
        super().__init__(fila)
        self.expresion = expresion

    def ejecutar(self, entorno: Entorno):
        if not self.expresion:
            self.generador.agregarSaltoLinea()
        else:
            # for expre in self.expresion:
            self.expresion.generador = self.generador
            self.expresion.ejecutar(entorno)
