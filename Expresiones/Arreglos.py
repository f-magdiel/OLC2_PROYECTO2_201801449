from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Arreglo(Expresion):
    def __init__(self, fila, expresiones):
        super().__init__(fila)
        self.expresiones = expresiones

    def convertir(self, generador, entorno):
        # ! Validar expresiones
        if not self.expresiones:
            valor = Valor(self.fila, [TipoPrimitivo.ARREGLO])
            valor.reference = generador.nuevoTemp()
            # ! Se genera código
            valor.codigo = f"\t// Arreglo\n" \
                           f"\t{valor.reference} = H;\n" \
                           f"\tHEAP[(int)H] = 0;\n" \
                           f"\tH = H + 1;\n\n"
            return valor
        else:
            pass
            # ? Falta para imprimir un arreglo lleno
