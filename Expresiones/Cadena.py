from Abstracta.Expresion import Expresion
from Entorno.Valor import Valor
from Entorno.Entorno import Entorno


class Cadena(Expresion):
    def __init__(self, fila, tipo, valor):
        super().__init__(fila)
        self.tipo = tipo
        self.valor = valor

    def ejecutar(self, entorno: Entorno):
        flag_cadena = False
        temp = self.generador.nuevoTemp()
        self.generador.agregarExpresion(temp, "P", "", "")
        valor = Valor(self.fila, temp, True, self.tipo)
        valor.listTemp.append(temp)

        # Recorrer la cadena
        for char in self.valor:
            if flag_cadena:
                flag_cadena = False
                temp = self.generador.nuevoTemp()
                self.generador.agregarExpresion(temp, "P", "", "")
                valor.listTemp.append(temp)

            elif char == '{':
                self.generador.agregarValorHeap("P", "-1")
                self.generador.sigHeap()
                continue
            elif char == '}':
                valor.listTemp.append("-1")
                flag_cadena = True
                continue
            else:
                self.generador.agregarValorHeap("P", str(ord(char)))
                self.generador.sigHeap()

        if not flag_cadena:
            self.generador.agregarValorHeap("P", "-1")
            self.generador.sigHeap()

        return valor
