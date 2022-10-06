from Abstracta.Instruccion import Instruccion


class Continue(Instruccion):
    def __init__(self, fila):
        super().__init__(fila)

    def convertir(self, generador, entorno):
        # ! Se genera tmp
        tmp1 = generador.nuevoTemp()
        # ! Se genera código
        codigo = f"\t/* SENTENCIA CONTINUE */\n" \
                 f"\t{tmp1} = S - TEMPORAL_CONTINUE;\n" \
                 f"\tS = S - {tmp1};\n" \
                 f"\tgoto ETIQUETA_CONTINUE;\n"
        return codigo
