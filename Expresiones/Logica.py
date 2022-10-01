from Abstracta.Expresion import Expresion
from Enum.OpLogico import OPERADOR_LOGICO
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Logica(Expresion):
    def __init__(self, fila, exp1, operador, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def convertir(self, entorno):
        # ! Convertir expres y obtener resultados al operar
        self.exp1.generador = self.generador
        self.exp2.generador = self.generador
        val_izq = self.exp1.convertir(entorno)
        val_der = self.exp2.convertir(entorno)

        if val_izq and val_der:
            if val_izq.tipo == TipoPrimitivo.BOOL and val_der.tipo == TipoPrimitivo.BOOL:
                nuevo_valor = Valor(self.fila, TipoPrimitivo.BOOL)
                # ! Es or
                if self.operador == OPERADOR_LOGICO.OR:
                    # ! Crear y asignar etiquetas
                    nuevo_valor.trueLabel = val_izq.trueLabel + ", " + val_der.trueLabel
                    nuevo_valor.falseLabel = val_der.falseLabel
                    nuevo_valor.codigo = val_izq.codigo + f"\t{val_izq.falseLabel}:\n" + val_der.codigo

                # ! Es and
                else:
                    nuevo_valor.trueLabel = val_der.trueLabel
                    nuevo_valor.falseLabel = val_izq.falseLabel + ", " + val_der.falseLabel
                    nuevo_valor.codigo = val_izq.codigo + f"\t{val_izq.trueLabel}:\n" + val_der.codigo

                return nuevo_valor
            else:
                print("Error")
        else:
            print("Error")
