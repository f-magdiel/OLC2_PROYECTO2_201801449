from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from Entorno.Valor import Valor
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class NewArreglo(Expresion):
    def __init__(self, fila, exp1, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2

    def convertir(self, generador, entorno):
        val_izq = self.exp1.convertir(generador, entorno)
        val_der = self.exp2.convertir(generador, entorno)

        if val_izq and val_der:
            if val_der.tipo[0] == TipoPrimitivo.I64:
                val_izq.tipo.insert(0, TipoPrimitivo.ARREGLO)
                valor = Valor(self.fila, val_izq.tipo)
                valor.reference = generador.nuevoTemp()

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
                # ! Se genera código
                valor.codigo += f"\t// CREAR ARREGLO\n" \
                                f"\t{valor.reference} = H; \n" \
                                f"\t{tmp1} = {val_der.reference} + 1;\n" \
                                f"\tH = H + {tmp1}; \n" \
                                f"\t{tmp2} = {valor.reference} + 0;\n" \
                                f"\tHEAP[(int){tmp2}] = {val_der.reference}; \n\n" \
                                f"\t \n" \
                                f"\t{tmp3} = 0; \n" \
                                f"\t{tmp4} = {valor.reference} + 0;\n" \
                                f"\t{tmp5} = HEAP[(int){tmp4}]; \n\n" \
                                f"\t{lbl3}:\n" \
                                f"\tif ({tmp3} < {tmp5}) goto {lbl1}; \n" \
                                f"\tgoto {lbl2};\n" \
                                f"\t{lbl1}:\n\n"
                # ! Tipo de valor interno
                if valor.tipo[0] != TipoPrimitivo.BOOL:
                    valor.codigo += f"\t \n" + val_izq.codigo + \
                                    f"\t{tmp6} = {valor.reference} + 1; \n" \
                                    f"\t{tmp7} = {tmp6} + {tmp3}; \n" \
                                    f"\tHEAP[(int){tmp7}] = {val_izq.reference}; \n\n"
                else:
                    lbl1 = generador.nuevoLabel()
                    #  ! Se genera código
                    valor.codigo += f"\t \n" + val_izq.codigo + \
                                    f"\t{val_izq.trueLabel}:\n" \
                                    f"\t{tmp6} = {valor.reference} + 1; \n" \
                                    f"\t{tmp7} = {tmp6} + {tmp3}; \n\n" \
                                    f"\tHEAP[(int){tmp7}] = 1; \n" \
                                    f"\tgoto {lbl1};\n" \
                                    f"\t{val_izq.falseLabel}:\n" \
                                    f"\t{tmp6} = {valor.reference} + 1; \n" \
                                    f"\t{tmp7} = {tmp6} + {tmp3}; \n\n" \
                                    f"\tHEAP[(int){tmp7}] = 0;\n" \
                                    f"\t{lbl1}:\n\n"

                valor.codigo += f"\t{tmp3} = {tmp3} + 1; \n" \
                                f"\tgoto {lbl3}; \n" \
                                f"\t{lbl2}:\n\n"

                return valor
            else:
                alert = "Error en los tipos del arreglo"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Error en los valores del arreglo"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
