from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from Entorno.Valor import Valor


class Bool(Expresion):
    def __init__(self, fila, tipo, valor):
        super().__init__(fila)
        self.tipo = tipo
        self.valor = valor

    def ejecutar(self, entorno: Entorno):
        pass
        false_lbl = self.generador.nuevoLabel()
        true_lbl = self.generador.nuevoLabel()

        codigo = f"if ({self.valor}) goto {true_lbl}\n" \
                 f"goto {false_lbl}"
        valor = Valor(self.fila, codigo, False, self.tipo)
        valor.falseLabel = false_lbl
        valor.trueLabel = true_lbl
        return valor
    
