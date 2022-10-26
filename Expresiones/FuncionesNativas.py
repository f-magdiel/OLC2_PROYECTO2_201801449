from Abstracta.Expresion import Expresion
from Enum.Nativas import NATIVAS
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class FuncionNativa(Expresion):
    def __init__(self, fila, funcion, expresion):
        super().__init__(fila)
        self.funcion = funcion
        self.expresion = expresion

    def convertir(self, generador, entorno):
        # ! Convertir la expresion y obtener los resultados
        valor = self.expresion.convertir(generador, entorno)

        if valor:
            # ! ABSOLUTO
            if self.funcion == NATIVAS.ABS:
                # ! F64, I64
                if valor.tipo[0] in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, valor.tipo)
                    tmp1 = generador.nuevoTemp()
                    nuevo_valor.reference = generador.nuevoTemp()
                    # ! Labels aux
                    lbl1 = generador.nuevoLabel()
                    lbl2 = generador.nuevoLabel()
                    lbl3 = generador.nuevoLabel()
                    # ! Se genera código
                    nuevo_valor.codigo = valor.codigo + f"\t// ABSOLUTO\n" \
                                                        f"\tif ({valor.reference} < 0) goto {lbl1};\n" \
                                                        f"\tgoto {lbl2};\n" \
                                                        f"\t{lbl1}:\n" \
                                                        f"\t{tmp1} = - 1;\n" \
                                                        f"\t{nuevo_valor.reference} = {valor.reference} * {tmp1};\n" \
                                                        f"\tgoto {lbl3};\n" \
                                                        f"\t{lbl2}:\n" \
                                                        f"\t{nuevo_valor.reference} = {valor.reference};\n" \
                                                        f"\t{lbl3}:\n"
                    return nuevo_valor
                else:
                    alert = "El tipo '{}' no posee la funcion nativa 'abs()'.".format(valor.tipo[0].value)
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            # ! SQRT
            elif self.funcion == NATIVAS.SQRT:
                # ! F64, I64
                if valor.tipo[0] in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, [TipoPrimitivo.F64])
                    nuevo_valor.reference = generador.nuevoTemp()
                    # ! Temporales aux
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    # ! Labels aux
                    lbl1 = generador.nuevoLabel()
                    lbl2 = generador.nuevoLabel()
                    lbl3 = generador.nuevoLabel()

                    nuevo_valor.codigo = valor.codigo + f"\t// SQRT\n" \
                                                        f"\t{nuevo_valor.reference} = {valor.reference} / 2;\n" \
                                                        f"\t{tmp1} = 0;\n" \
                                                        f"\t{lbl3}:\n" \
                                                        f"\tif ({nuevo_valor.reference} != {tmp1}) goto {lbl1};\n" \
                                                        f"\tgoto {lbl2};\n" \
                                                        f"\t{lbl1}:\n" \
                                                        f"\t{tmp1} = {nuevo_valor.reference};\n" \
                                                        f"\t{tmp2} = {valor.reference} / {tmp1};\n" \
                                                        f"\t{tmp3} = {tmp2} + {tmp1};\n" \
                                                        f"\t{nuevo_valor.reference} = {tmp3} / 2;\n" \
                                                        f"\tgoto {lbl3};\n" \
                                                        f"\t{lbl2}:\n"
                    return nuevo_valor
                else:
                    alert = "Error no tiene la función nativa 'sqrt()'.".format(valor.tipo[0].value)
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            # ! TOW, TOS
            elif self.funcion in [NATIVAS.TOOWNED, NATIVAS.TOSTRING]:
                # ! STR, STRING
                if valor.tipo[0] in [TipoPrimitivo.STRING, TipoPrimitivo.STR]:
                    valor.tipo[0] = TipoPrimitivo.STRING
                    return valor
                else:
                    alert = "Error no tiene la función nativa 'tostring'".format(valor.tipo[0].value)
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            # ! CLONE
            else:
                # ! CUANDO NO ES ARREGLO/VECTOR
                if valor.tipo[0] not in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                    return valor
                else:
                    return valor

        else:
            alert = "Error en las expresiones de funciones nativas"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
