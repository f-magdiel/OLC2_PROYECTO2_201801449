from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class VectorUnico(Expresion):
    def __init__(self, fila, expresion=None):
        super().__init__(fila)
        self.expresion = expresion

    def convertir(self, generador, entorno):
        if self.expresion is None:
            valor = Valor(self.fila, [TipoPrimitivo.VECTOR])
            valor.reference = generador.nuevoTemp()
            # ! Temporales aux
            tmp1 = generador.nuevoTemp()
            tmp2 = generador.nuevoTemp()
            # ! Se genera código
            valor.codigo += f"\t// Vector new()\n" \
                            f"\t{valor.reference} = H; // ref\n" \
                            f"\tH = H + 2; // Reservar espacio\n" \
                            f"\t{tmp1} = {valor.reference} + 0;\n" \
                            f"\tHEAP[(int){tmp1}] = 0; // len\n" \
                            f"\t{tmp2} = {valor.reference} + 1;\n" \
                            f"\tHEAP[(int){tmp2}] = 1; // capacity\n\n"

            return valor
        else:
            valor_cap = self.expresion.convertir(generador, entorno)
            if valor_cap:
                if valor_cap.tipo[0] == TipoPrimitivo.I64:
                    valor = Valor(self.fila, [TipoPrimitivo.VECTOR])
                    valor.reference = generador.nuevoTemp()
                    # ! Temporales aux
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # ! Se genera código
                    valor.codigo += f"\t// Vector with_capacity()\n" \
                                    f"\t{valor.reference} = H; // ref\n" \
                                    f"\tH = H + 2; // Reservar espacio\n" \
                                    f"\t{tmp1} = {valor.reference} + 0;\n" \
                                    f"\tHEAP[(int){tmp1}] = 0; // len\n\n" \
                                    f"\t// Capacidad\n" + valor_cap.codigo + \
                                    f"\t{tmp2} = {valor.reference} + 1;\n" \
                                    f"\tHEAP[(int){tmp2}] = {valor_cap.reference}; // capacity\n\n"
                    return valor
                else:
                    print("Error")
            else:
                print("Error en exp")
