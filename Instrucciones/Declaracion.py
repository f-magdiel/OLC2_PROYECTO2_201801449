from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Variable import Variable


class Declaracion(Instruccion):
    def __init__(self, fila, tipo, id, expresion, mutable):
        super().__init__(fila)
        self.mutable = mutable
        self.tipo = tipo
        self.id = id
        self.expresion = expresion

    def convertir(self, entorno):
        self.expresion.generador = self.generador

        valor = self.expresion.convertir(entorno)

        if valor:

            if self.tipo == TipoPrimitivo.NULO:
                print("SIIII")
                variable = Variable(self.fila, self.mutable, self.id, valor.tipo)
                entorno.nueva_variable(variable)

                if valor.tipo != TipoPrimitivo.BOOL:
                    tmp1 = self.generador.nuevoTemp()
                    codigo = f"\t/* DECLARACIÓN */\n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion};\n" \
                                                                       f"\tSTACK[(int){tmp1}] = {valor.reference};\n"
                    return codigo
                else:

                    tmp1 = self.generador.nuevoTemp()
                    lbl1 = self.generador.nuevoLabel()

                    codigo = f"\t/* DECLARACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                       f"\t{tmp1} = S + {variable.posicion};\n" \
                                                                       f"\tSTACK[(int){tmp1}] = 1;\n" \
                                                                       f"\tgoto {lbl1};\n" \
                                                                       f"\t{valor.falseLabel}:\n" \
                                                                       f"\t{tmp1} = S + {variable.posicion};\n" \
                                                                       f"\tSTACK[(int){tmp1}] = 0;\n" \
                                                                       f"\t{lbl1}:\n"
                    return codigo
            else:
                pass
        else:
            print("Error")
