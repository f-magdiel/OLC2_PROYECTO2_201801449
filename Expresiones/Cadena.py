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
        self.generador.agregarExpresion(temp, "P", "", "")
        # Recorrer la cadena
        for char in self.valor:
            if char == '{':
                self.generador.agregarValorHeap("P", "-2")
                self.generador.sigHeap()
            elif char == '}':
                continue
            else:
                self.generador.agregarValorHeap("P", str(ord(char)))
                self.generador.sigHeap()
        # Agregar el final de cadena
        self.generador.agregarValorHeap("P", "-1")
        self.generador.sigHeap()
        # Retornar el VALOR
        return Valor(self.fila, temp, True, self.tipo)
