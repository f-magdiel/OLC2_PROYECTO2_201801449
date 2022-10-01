from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Relacional(Expresion):
    def __init__(self, fila, exp1, operador, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def convertir(self, entorno):
        # ! Convertir las expres y obtener resultados operados
        self.exp1.generador = self.generador
        self.exp2.generador = self.generador
        val_izq = self.exp1.convertir(entorno)
        val_der = self.exp2.convertir(entorno)

        if val_izq and val_der:
            if val_izq.tipo == val_der.tipo and val_izq.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64, TipoPrimitivo.STR]:
                nuevo_valor = Valor(self.fila, TipoPrimitivo.BOOL)
                trueLabel = self.generador.nuevoLabel()
                falseLabel = self.generador.nuevoLabel()

                nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_izq.reference} {self.operador} {val_der.reference}) goto {trueLabel};\n" \
                                                                        f"\tgoto {falseLabel};\n"
                nuevo_valor.trueLabel = trueLabel
                nuevo_valor.falseLabel = falseLabel
                return nuevo_valor
            else:
                print("Error")
        else:
            print("Error")
