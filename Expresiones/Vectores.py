from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Vector(Expresion):
    def __init__(self, fila, expresiones):
        super().__init__(fila)
        self.expresiones = expresiones

    def convertir(self, generador, entorno):
        if self.expresiones:
            valores = []
            for i in range(len(self.expresiones)):
                valores.append(self.expresiones[i].convertir(generador, entorno))

            if None not in valores:
                tipo = valores[0].tipo
                flag_correcto = True
                for valor in valores:
                    if len(valor.tipo) == len(tipo):
                        for i in range(len(tipo)):
                            if valor.tipo[i] != tipo[i]:
                                flag_correcto = False
                                break
                        if not flag_correcto:
                            break
                    else:
                        flag_correcto = False
                        break

                if flag_correcto:
                    tipo.insert(0, TipoPrimitivo.VECTOR)
                    valor = Valor(self.fila, tipo)
                    valor.reference = generador.nuevoTemp()

                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()

                    valor.codigo += f"\t// VECTOR\n" \
                                    f"\t{valor.reference} = H; \n" \
                                    f"\tH = H + {len(valores) + 2}; \n" \
                                    f"\t{tmp1} = {valor.reference} + 0;\n" \
                                    f"\tHEAP[(int){tmp1}] = {len(valores)}; \n" \
                                    f"\t{tmp2} = {valor.reference} + 1;\n" \
                                    f"\tHEAP[(int){tmp2}] = {len(valores) + 1}; \n\n"

                    for i in range(len(valores)):
                        if tipo[1] == TipoPrimitivo.BOOL:
                            tmp1 = generador.nuevoTemp()
                            lbl1 = generador.nuevoLabel()

                            valor.codigo += f"\t \n" + valores[i].codigo + \
                                            f"\t{valores[i].lt}:\n" \
                                            f"\t{tmp1} = {valor.reference} + {i + 2};\n" \
                                            f"\tHEAP[(int){tmp1}] = 1;\n" \
                                            f"\tgoto {lbl1};\n" \
                                            f"\t{valores[i].lf}:\n" \
                                            f"\t{tmp1} = {valor.reference} + {i + 2};\n" \
                                            f"\tHEAP[(int){tmp1}] = 0;\n" \
                                            f"\t{lbl1}:\n\n"
                        else:
                            tmp1 = generador.nuevoTemp()
                            valor.codigo += f"\t \n" + valores[i].codigo + \
                                            f"\t{tmp1} = {valor.reference} + {i + 2};\n" \
                                            f"\tHEAP[(int){tmp1}] = {valores[i].reference};\n\n"

                    return valor
                else:
                    alert = "Error tipos incompatibles en VECTOR"
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            else:
                alert = "Error no puede venir tipos NULOS en VECTOR"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Error en expresiones de VECTOR"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
