from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Variable import Variable
from Tipo.ArrayTipo import ArrayTipo


class Declaracion(Instruccion):
    def __init__(self, fila, tipo, id, expresion, mutable):
        super().__init__(fila)
        self.mutable = mutable
        self.tipo = tipo
        self.id = id
        self.expresion = expresion

    def convertir(self, generador, entorno):
        valor = self.expresion.convertir(generador, entorno)
        if valor:
            # ! Cuando el tipo no viene especificado

            if self.tipo == TipoPrimitivo.NULO:
                return self.declarar_variable(generador, entorno, valor, valor.tipo)
            else:
                # ! Cuando el tipo viene especificado
                if isinstance(self.tipo, ArrayTipo):
                    return self.declarar_variable(generador, entorno, valor, self.tipo.obtener_tipo())
                else:
                    return self.declarar_variable(generador, entorno, valor, [self.tipo])
        else:
            print("Error en valor")

    def declarar_variable(self, generador, entorno, valor, tipo):
        var = Variable(self.fila, self.id, self.mutable, tipo)
        entorno.nueva_variable(var)

        if valor.tipo[0] != TipoPrimitivo.BOOL:
            tmp1 = generador.nuevoTemp()
            codigo = f"\t/* DECLARACIÓN */\n" + valor.codigo + f"\t{tmp1} = S + {var.posicion};\n" \
                                                               f"\tSTACK[(int){tmp1}] = {valor.reference};\n"
            return codigo
        else:
            tmp1 = generador.nuevoTemp()
            lbl1 = generador.nuevoLabel()

            codigo = f"\t/* DECLARACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                               f"\t{tmp1} = S + {var.posicion};\n" \
                                                               f"\tSTACK[(int){tmp1}] = 1;\n" \
                                                               f"\tgoto {lbl1};\n" \
                                                               f"\t{valor.falseLabel}:\n" \
                                                               f"\t{tmp1} = S + {var.posicion};\n" \
                                                               f"\tSTACK[(int){tmp1}] = 0;\n" \
                                                               f"\t{lbl1}:\n"
            return codigo
