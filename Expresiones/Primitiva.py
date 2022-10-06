from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Primitiva(Expresion):
    def __init__(self, fila, tipo, valor):
        super().__init__(fila)
        self.tipo = tipo
        self.valor = valor

    def convertir(self, generador, entorno):
        valor = Valor(self.fila, [self.tipo])

        # ! Validar el tipo
        if self.tipo in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
            # ! Hacer referencia al valor
            valor.reference = self.valor
            return valor
        elif self.tipo == TipoPrimitivo.CHAR:
            # ! Hacer referencia al valor
            valor.reference = str(ord(self.valor))
            return valor
        elif self.tipo == TipoPrimitivo.BOOL:
            # ! Crear labels
            valor.trueLabel = generador.nuevoLabel()
            valor.falseLabel = generador.nuevoLabel()
            # ! Generar código
            valor.codigo = f"\tif ({self.valor}) goto {valor.trueLabel};\n" \
                           f"\tgoto {valor.falseLabel};\n"
            # ! Retornar
            return valor
        elif self.tipo == TipoPrimitivo.STR:
            # ! Valor reference
            valor.reference = generador.nuevoTemp()
            # ! Se genera código
            valor.codigo = f"\t{valor.reference} = H;\n"
            # ! Insetar en lista de temps
            valor.listTemp.append(valor.reference)
            # ! Se realiza formateo general
            cadena = self.valor.replace("{:?}", "{}")

            flag_cadena = False
            # ! Recorrer la cadena
            for char in cadena:
                # ! Validar flag cadena
                if flag_cadena:
                    # ! Se genera temporal
                    tmp = generador.nuevoTemp()
                    # ! Se genera codigo referencia
                    valor.codigo += f"\t{tmp} = H;\n"
                    valor.listTemp.append(tmp)
                    flag_cadena = False
                # ! Validar caracter especial
                if char == '{':
                    valor.codigo += f"\tHEAP[(int)H] = - 1;\n" \
                                    f"\tH = H + 1;\n"
                    continue
                elif char == '}':
                    # ! El -1 indica sustitución por formateo en lista
                    valor.listTemp.append(-1)
                    flag_cadena = True
                    continue
                else:
                    valor.codigo += f"\tHEAP[(int)H] = {ord(char)};\n" \
                                    f"\tH = H + 1;\n"

            if not flag_cadena:
                valor.codigo += f"\tHEAP[(int)H] = - 1;\n" \
                                f"\tH = H + 1;\n"

            return valor
