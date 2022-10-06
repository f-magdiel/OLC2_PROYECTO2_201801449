from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Relacional(Expresion):
    def __init__(self, fila, exp1, operador, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def convertir(self, generador, entorno):
        # ! Convertir las expres y obtener resultados operados
        val_izq = self.exp1.convertir(generador, entorno)
        val_der = self.exp2.convertir(generador, entorno)

        if val_izq and val_der:
            if val_izq.tipo[0] == val_der.tipo[0] and val_izq.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64, TipoPrimitivo.STR]:
                nuevo_valor = Valor(self.fila, [TipoPrimitivo.BOOL])
                nuevo_valor.trueLabel = generador.nuevoLabel()
                nuevo_valor.falseLabel = generador.nuevoLabel()
                # ! Se genera código
                nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_izq.reference} {self.operador} {val_der.reference}) goto {nuevo_valor.trueLabel};\n" \
                                                                        f"\tgoto {nuevo_valor.falseLabel};\n"
                return nuevo_valor
            else:
                print("Error expresiones incompatibles")
        else:
            print("Error en expresiones")
