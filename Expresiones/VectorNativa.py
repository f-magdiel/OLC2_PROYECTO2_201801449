from Abstracta.Expresion import Expresion
from Enum.Nativas import NATIVAS
from Entorno.Valor import Valor
from Enum.TipoPrimitivo import TipoPrimitivo


class VectorNativa(Expresion):
    def __init__(self, fila, exp1, funcion, exp2=None):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.funcion = funcion

    def convertir(self, generador, entorno):
        valor_arr = self.exp1.convertir(generador, entorno)

        if valor_arr:
            if valor_arr.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                # ! Aplica a LEN
                if self.funcion == NATIVAS.LEN:
                    valor = Valor(self.fila, [TipoPrimitivo.I64])
                    tmp1 = generador.nuevoTemp()
                    valor.reference = generador.nuevoTemp()
                    valor.codigo = valor_arr.codigo + f"\t// len()\n" \
                                                      f"\t{tmp1} = {valor_arr.reference} + 0;\n" \
                                                      f"\t{valor.reference} = HEAP[(int){tmp1}];\n\n"
                    return valor

                # ! Aplica a CONTAINS
                elif self.funcion == NATIVAS.CONTAINS:
                    if valor_arr.tipo[0] == TipoPrimitivo.VECTOR:

                        if len(valor_arr.tipo) > 1 and valor_arr.tipo[1] not in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                            valor_cont = self.exp2.convertir(generador, entorno)
                            if valor_cont:
                                if valor_cont.tipo[0] not in [TipoPrimitivo.VECTOR, TipoPrimitivo.ARREGLO]:
                                    valor = Valor(self.fila, [TipoPrimitivo.BOOL])
                                    # ! Temporales aux
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    tmp3 = generador.nuevoTemp()
                                    tmp4 = generador.nuevoTemp()
                                    tmp5 = generador.nuevoTemp()
                                    tmp6 = generador.nuevoTemp()
                                    tmp7 = generador.nuevoTemp()
                                    # ! Labels aux
                                    lbl1 = generador.nuevoLabel()
                                    lbl2 = generador.nuevoLabel()
                                    lbl3 = generador.nuevoLabel()

                                    valor.codigo = valor_arr.codigo + f"\t// contains()\n" \
                                                                      f"\t{tmp1} = 0; // Bandera\n\n" \
                                                                      f"\t// Recorrer vector\n" \
                                                                      f"\t{tmp2} = 0; // i\n" \
                                                                      f"\t{tmp3} = {valor_arr.reference} + 0;\n" \
                                                                      f"\t{tmp4} = HEAP[(int){tmp3}]; // len\n\n" \
                                                                      f"\t{lbl3}:\n" \
                                                                      f"\tif ({tmp2} < {tmp4}) goto {lbl1}; // i < len\n" \
                                                                      f"\tgoto {lbl2};\n" \
                                                                      f"\t{lbl1}:\n" \
                                                                      f"\t{tmp5} = {valor_arr.reference} + 2; // Puntero valores\n" \
                                                                      f"\t{tmp6} = {tmp5} + {tmp2}; // Dir. valor\n" \
                                                                      f"\t{tmp7} = HEAP[(int){tmp6}]; // Valor\n\n"
                                    # ! Validar tipos
                                    if valor_arr.tipo[1] not in [TipoPrimitivo.STR, TipoPrimitivo.BOOL]:
                                        valor.codigo += valor_cont.codigo

                                        trueLabel = generador.nuevoLabel()
                                        falseLabel = generador.nuevoLabel()

                                        valor.codigo += f"\tif ({tmp7} == {valor_cont.reference}) goto {trueLabel};\n" \
                                                        f"\tgoto {falseLabel};\n" \
                                                        f"\t{trueLabel}:\n" \
                                                        f"\t{tmp1} = 1;\n" \
                                                        f"\t{falseLabel}:\n\n"

                                    elif valor_arr.tipo[1] == TipoPrimitivo.BOOL:
                                        tmp8 = generador.nuevoTemp()
                                        trueLabel = generador.nuevoLabel()
                                        falseLabel = generador.nuevoLabel()

                                        valor.codigo += f"\t{tmp8} = 0;\n" + valor_cont.codigo + \
                                                        f"\t{valor_cont.trueLabel}:\n" \
                                                        f"\t{tmp8} = 1;\n" \
                                                        f"\t{valor_cont.falseLable}:\n\n" \
                                                        f"\tif ({tmp7} == {tmp8}) goto {trueLabel};\n" \
                                                        f"\tgoto {falseLabel};\n" \
                                                        f"\t{trueLabel}:\n" \
                                                        f"\t{tmp1} = 1;\n" \
                                                        f"\t{falseLabel}:\n\n"
                                    else:
                                        valor.codigo += valor_cont.codigo
                                        # ! Temporales aux
                                        tmp8 = generador.nuevoTemp()
                                        tmp9 = generador.nuevoTemp()
                                        tmp10 = generador.nuevoTemp()
                                        tmp11 = generador.nuevoTemp()
                                        tmp12 = generador.nuevoTemp()
                                        tmp13 = generador.nuevoTemp()
                                        # ! Labels aux
                                        lbl4 = generador.nuevoLabel()
                                        lbl5 = generador.nuevoLabel()
                                        lbl6 = generador.nuevoLabel()
                                        lbl7 = generador.nuevoLabel()
                                        lbl8 = generador.nuevoLabel()
                                        lbl9 = generador.nuevoLabel()
                                        lbl10 = generador.nuevoLabel()
                                        lbl11 = generador.nuevoLabel()

                                        valor.codigo += f"\t{tmp8} = {tmp7}; // i\n" \
                                                        f"\t{tmp9} = {valor_cont.reference}; // j\n\n" \
                                                        f"\t{tmp10} = - 1; // Para comparar fin\n" \
                                                        f"\t{lbl10}:\n" \
                                                        f"\t{tmp11} = HEAP[(int){tmp8}]; // char1\n" \
                                                        f"\t{tmp12} = HEAP[(int){tmp9}]; // char2\n\n" \
                                                        f"\tif ({tmp11} == {tmp12}) goto {lbl4};\n" \
                                                        f"\tgoto {lbl5};\n" \
                                                        f"\t{lbl4}: // Cad1 llego a fin?\n" \
                                                        f"\tif ({tmp11} == {tmp10}) goto {lbl6};\n" \
                                                        f"\tgoto {lbl7};\n" \
                                                        f"\t{lbl6}: // Cad2 llego a fin?\n" \
                                                        f"\tif ({tmp12} == {tmp10}) goto {lbl8};\n" \
                                                        f"\tgoto {lbl9};\n" \
                                                        f"\t{lbl8}: // Son iguales \n" \
                                                        f"\t{tmp1} = 1;\n" \
                                                        f"\tgoto {lbl11};\n" \
                                                        f"\t{lbl9}: // No son iguales\n" \
                                                        f"\tgoto {lbl11};\n" \
                                                        f"\t{lbl7}: // Sig. char\n" \
                                                        f"\t{tmp8} = {tmp8} + 1; // i++\n" \
                                                        f"\t{tmp9} = {tmp9} + 1; // j++\n" \
                                                        f"\tgoto {lbl10};\n" \
                                                        f"\t{lbl5}: // No son iguales\n" \
                                                        f"\t{lbl11}:\n\n"

                                        trueLabel = generador.nuevoLabel()
                                        falseLabel = generador.nuevoLabel()

                                        valor.codigo += f"\t// Verificar bandera\n" \
                                                        f"\tif ({tmp1}) goto {trueLabel};\n" \
                                                        f"\tgoto {falseLabel};\n" \
                                                        f"\t{trueLabel}:\n" \
                                                        f"\tgoto {lbl2};\n" \
                                                        f"\t{falseLabel}:\n\n"

                                        valor.codigo += f"\t{tmp2} = {tmp2} + 1; // i++\n" \
                                                        f"\tgoto {lbl3}; // Sig. pos\n" \
                                                        f"\t{lbl2}:\n\n"

                                        valor.trueLabel = generador.nuevoLabel()
                                        valor.falseLabel = generador.nuevoLabel()

                                        valor.codigo += f"\tif ({tmp1}) goto {valor.trueLabel};\n" \
                                                        f"\tgoto {valor.falseLabel};\n"
                                        return valor
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    # ! CAPACITY
                    if valor_arr.tipo[0] == TipoPrimitivo.VECTOR:
                        valor = Valor(self.fila, [TipoPrimitivo.I64])
                        tmp1 = generador.nuevoTemp()

                        valor.reference = generador.nuevoTemp()
                        valor.codigo = valor_arr.codigo + f"\t// len()\n" \
                                                          f"\t{tmp1} = {valor_arr.reference} + 1;\n" \
                                                          f"\t{valor.reference} = HEAP[(int){tmp1}];\n\n"
                        return valor
                    else:
                        print("Error")
            else:
                pass
        else:
            pass
