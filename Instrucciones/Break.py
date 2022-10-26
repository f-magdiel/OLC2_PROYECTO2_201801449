from Abstracta.Instruccion import Instruccion


class Break(Instruccion):
    def __init__(self, fila, expresion=None):
        super().__init__(fila)
        self.expresion = expresion

    def convertir(self, generador, entorno):
        # if not self.expresion:
        tmp1 = generador.nuevoTemp()
        # ! Se genera código
        codigo = f"\t // BREAK\n" \
                 f"\t{tmp1} = S - TEMPORAL_BREAK;\n" \
                 f"\tS = S - {tmp1};\n" \
                 f"\tgoto ETIQUETA_BREAK;\n"

        return codigo
        # else:
        #     # TODO: falta expresion
        #     pass
