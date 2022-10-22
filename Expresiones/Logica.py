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

    def convertir(self, generador, entorno):
        # ! Convertir expres y obtener resultados al operar
        val_izq = self.exp1.convertir(generador, entorno)
        val_der = self.exp2.convertir(generador, entorno)
        if val_izq and val_der:
            if val_izq.tipo[0] == TipoPrimitivo.BOOL and val_der.tipo[0] == TipoPrimitivo.BOOL:
                nuevo_valor = Valor(self.fila, [TipoPrimitivo.BOOL])
                # ! ES OR
                if self.operador == OPERADOR_LOGICO.OR:
                    # ! Crear y asignar etiquetas
                    nuevo_valor.trueLabel = val_izq.trueLabel + ":\n\t" + val_der.trueLabel
                    nuevo_valor.falseLabel = val_der.falseLabel
                    # ! Se genera código
                    nuevo_valor.codigo = val_izq.codigo + f"\t{val_izq.falseLabel}:\n" + val_der.codigo

                # ! ES AND
                else:
                    # ! Crear y asignar etiquetas
                    nuevo_valor.trueLabel = val_der.trueLabel
                    nuevo_valor.falseLabel = val_izq.falseLabel + ":\n\t" + val_der.falseLabel
                    # ! Se genera código
                    nuevo_valor.codigo = val_izq.codigo + f"\t{val_izq.trueLabel}:\n" + val_der.codigo

                return nuevo_valor
            else:
                print("Error no es tipo bool")
        else:
            print("Error EN EXPRESIONES")
