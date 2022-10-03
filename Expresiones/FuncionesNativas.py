from Abstracta.Expresion import Expresion
from Enum.Nativas import NATIVAS
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class FuncionNativa(Expresion):
    def __init__(self, fila, funcion, expresion):
        super().__init__(fila)
        self.funcion = funcion
        self.expresion = expresion

    def convertir(self, generador, entorno):
        # ! Convertir la expresion y obtener los resultados
        valor = self.expresion.convertir(generador, entorno)

        if valor:
            # ! Absoluto
            if valor.tipo == NATIVAS.ABS:
                if valor.tipo in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, valor.tipo)
                    tmp1 = generador.nuevoTemp()
                    tmp = generador.nuevoTemp()
                    nuevo_valor.reference = tmp

                    lbl1 = generador.nuevoLabel()
                    lbl2 = generador.nuevoLabel()
                    lbl3 = generador.nuevoLabel()
                    lbl4 = generador.nuevoLabel()

                    nuevo_valor.codigo = valor.codigo + f"\t{tmp1} = - 1; // Para operar\n" \
                                                        f"\tif ({valor.reference} < 0) goto {lbl1};\n" \
                                                        f"\tgoto {lbl2};\n" \
                                                        f"\t{lbl1}:\n" \
                                                        f"\t{tmp} = {valor.reference} * {tmp1};\n" \
                                                        f"\tgoto {lbl3};\n" \
                                                        f"\t{lbl2}:\n" \
                                                        f"\t{tmp} = {valor.reference};\n" \
                                                        f"\t{lbl3}:\n"
                    return nuevo_valor
                else:
                    print("Error")
            # ! Sqrt
            elif self.funcion == NATIVAS.SQRT:
                if valor.tipo in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, TipoPrimitivo.I64)
                    tmp = generador.nuevoTemp()
                    nuevo_valor.reference = tmp

                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()

                    lbl1 = generador.nuevoLabel()
                    lbl2 = generador.nuevoLabel()
                    lbl3 = generador.nuevoLabel()

                    nuevo_valor.codigo = valor.codigo + f"\t{tmp} = {valor.reference} / 2;\n" \
                                                        f"\t{tmp1} = 0;\n" \
                                                        f"\t{lbl3}:\n" \
                                                        f"\tif ({tmp} != {tmp1}) goto {lbl1};\n" \
                                                        f"\tgoto {lbl2};\n" \
                                                        f"\t{lbl1}:\n" \
                                                        f"\t{tmp1} = {tmp};\n" \
                                                        f"\t{tmp2} = {valor.reference} / {tmp1};\n" \
                                                        f"\t{tmp3} = {tmp2} + {tmp1};\n" \
                                                        f"\t{tmp} = {tmp3} / 2;\n" \
                                                        f"\tgoto {lbl3};\n" \
                                                        f"\t{lbl2}:\n"
                    return nuevo_valor
                else:
                    print("Error")
            # ! tow, tos
            elif self.funcion in [NATIVAS.TOOWNED, NATIVAS.TOSTRING]:
                if valor.tipo == TipoPrimitivo.STR:
                    valor.tipo = TipoPrimitivo.STRING
                    return valor
                else:
                    print("Error")
            # ! Clone
            else:
                if valor.tipo not in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                    return valor
                else:
                    pass
                    # TODO: falta
                    # ? Falta implementarlo

        else:
            print("Erro en expresion")
