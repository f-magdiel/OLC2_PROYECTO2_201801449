from Abstracta.Expresion import Expresion
from Entorno.Valor import Valor
from Entorno.Entorno import Entorno


class Cadena(Expresion):
    def __init__(self, fila, tipo, valor):
        super().__init__(fila)
        self.tipo = tipo
        self.valor = valor

    def ejecutar(self, entorno: Entorno):
        temp = self.generador.nuevoTemp()
        self.generador.agregarExpresion(temp, "H", "", "")
        # Recorrer la cadena
        for c in self.valor:
            self.generador.agregarValorHeap("H", str(ord(c)))
            self.generador.sigHeap()
        # Agregar el final de cadena
        self.generador.agregarValorHeap("H", "-1")
        # Retornar el VALOR
        return Valor(self.fila, temp, True, self.tipo)
