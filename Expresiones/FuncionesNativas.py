from Abstracta.Expresion import Expresion
from Enum.Nativas import NATIVAS
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class FuncionNativa(Expresion):
    def __init__(self, fila, funcion, expresion):
        super().__init__(fila)
        self.funcion = funcion
        self.expresion = expresion

    def convertir(self, entorno):
        # ! Convertir la expresion y obtener los resultados
        self.expresion.generador = self.generador
        valor = self.expresion.convertir(entorno)

        if valor:
            # ! Absoluto
            if valor.tipo == NATIVAS.ABS:
                if valor.tipo in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, valor.tipo)
                    tmp1 = self.generador.nuevoTemp()
                    tmp = self.generador.nuevoTemp()
                    nuevo_valor.reference = tmp

                    lbl1 = self.generador.nuevoLabel()
                    lbl2 = self.generador.nuevoLabel()
                    lbl3 = self.generador.nuevoLabel()
                    lbl4 = self.generador.nuevoLabel()

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
                    tmp = self.generador.nuevoTemp()
                    nuevo_valor.reference = tmp

                    tmp1 = self.generador.nuevoTemp()
                    tmp2 = self.generador.nuevoTemp()
                    tmp3 = self.generador.nuevoTemp()

                    lbl1 = self.generador.nuevoLabel()
                    lbl2 = self.generador.nuevoLabel()
                    lbl3 = self.generador.nuevoLabel()

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
                if valor.tipo in [TipoPrimitivo.TOS, TipoPrimitivo.TOW]:
                    valor.tipo = TipoPrimitivo.TOS
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
