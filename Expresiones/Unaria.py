from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Enum.OpUnario import OPERADOR_UNARIO
from Entorno.Entorno import Entorno
from Entorno.Valor import Valor


class Unaria(Expresion):
    def __init__(self, fila, operador, expresion):
        super().__init__(fila)
        self.operador = operador
        self.expresion = expresion

    def convertir(self, entorno: Entorno):
        self.expresion.generador = self.generador
        valor = self.expresion.convertir(entorno)

        if valor:
            # ! menos
            if self.operador == OPERADOR_UNARIO.MENOS:
                # ! para f64,i64
                if valor.tipo in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, valor.tipo)
                    tmp = self.generador.nuevoTemp()
                    nuevo_valor.reference = tmp
                    nuevo_valor.codigo = valor.codigo + f"\t{tmp} = - {valor.reference};\n"
                    return nuevo_valor
                else:
                    print("Error")
            # ! not
            else:
                # ! Bool
                if valor.tipo == TipoPrimitivo.BOOL:
                    nuevo_valor = Valor(self.fila, valor.tipo)
                    nuevo_valor.codigo = valor.codigo
                    nuevo_valor.trueLabel = valor.trueLabel
                    nuevo_valor.falseLabel = valor.falseLabel
                    return nuevo_valor
                else:
                    print("Error")
        else:
            print("Error")
