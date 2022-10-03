from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor
from Entorno.Entorno import Entorno


class Primitiva(Expresion):
    def __init__(self, fila, tipo, valor):
        super().__init__(fila)
        self.tipo = tipo
        self.valor = valor

    def convertir(self, entorno):
        valor = Valor(self.fila, self.tipo)
        # ! validar el tipo
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
            trueLabel = self.generador.nuevoLabel()
            falseLabel = self.generador.nuevoLabel()
            # ! Generar código
            valor.codigo = f"\tif ({self.valor}) goto {trueLabel};\n" \
                           f"\tgoto {falseLabel};\n"
            # ! Asignar valores
            valor.trueLabel = trueLabel
            valor.falseLabel = falseLabel
            return valor

        elif self.tipo == TipoPrimitivo.STR:
            # ! devuelve un tmp y un listado de tmps si se formatea
            cadena = self.valor.replace("{:?}", "{}")
            flag_cadena = False
            # ! Asignar tmp para la cadena
            tmp = self.generador.nuevoTemp()
            valor.reference = tmp
            valor.codigo = f"\t{tmp} = H;\n"
            valor.listTemp.append(tmp)

            # ! Recorrer la cadena
            for char in cadena:
                # ! Validar flag cadena
                if flag_cadena:
                    flag_cadena = False
                    tmp = self.generador.nuevoTemp()
                    valor.codigo += f"\t{tmp} = H;\n"
                    valor.listTemp.append(tmp)
                # ! Validar caracter especial
                if char == '{':
                    valor.codigo += f"\tHEAP[(int)H] = - 1;\n" \
                                    f"\tH = H + 1;\n"
                    continue

                elif char == '}':
                    # ! El -1 indica sustitución por formateo
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
