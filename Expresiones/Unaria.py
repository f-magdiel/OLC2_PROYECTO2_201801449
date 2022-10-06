from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Enum.OpUnario import OPERADOR_UNARIO

from Entorno.Valor import Valor


class Unaria(Expresion):
    def __init__(self, fila, operador, expresion):
        super().__init__(fila)
        self.operador = operador
        self.expresion = expresion

    def convertir(self, generador, entorno):
        # ! Se genera valor a retornar
        valor = self.expresion.convertir(generador, entorno)
        if valor:
            # ! menos
            if self.operador == OPERADOR_UNARIO.MENOS:
                # ! para f64,i64
                if valor.tipo[0] in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, valor.tipo)
                    nuevo_valor.reference = generador.nuevoTemp()
                    nuevo_valor.codigo = valor.codigo + f"\t{nuevo_valor.reference} = - {valor.reference};\n"
                    return nuevo_valor
                else:
                    print("Error al operar")
            # ! not
            else:
                # ! Bool
                if valor.tipo[0] == TipoPrimitivo.BOOL:
                    nuevo_valor = Valor(self.fila, [TipoPrimitivo.BOOL])
                    # ! Se copia el código
                    nuevo_valor.codigo = valor.codigo
                    # ! Se intercambian las etiquetas
                    nuevo_valor.trueLabel = valor.falseLabel
                    nuevo_valor.falseLabel = valor.trueLabel
                    return nuevo_valor
                else:
                    print("Error al operar")
        else:
            print("Error en la expresion")
