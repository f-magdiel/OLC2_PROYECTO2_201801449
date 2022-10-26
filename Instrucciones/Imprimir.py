from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Imprimir(Instruccion):
    def __init__(self, fila, expresiones):
        super().__init__(fila)
        self.expresiones = expresiones

    def convertir(self, generador, entorno):
        if not self.expresiones:
            codigo = f"\t \n" \
                     f"\tprintf(\"%c\", 10);\n"
            return codigo
        else:
            valor_str = self.expresiones[0].convertir(generador, entorno)
            if valor_str:
                if valor_str.tipo[0] == TipoPrimitivo.STR:
                    if len(self.expresiones) - 1 == valor_str.listTemp.count(-1):
                        codigo = f"\t// IMPRIMIR \n" + valor_str.codigo
                        flag_error = False
                        valores = []
                        for i in range(1, len(self.expresiones)):
                            valor = self.expresiones[i].convertir(generador, entorno)
                            if valor:
                                valores.append(valor)
                            else:
                                flag_error = True
                                break
                        if not flag_error:

                            if len(valor_str.listTemp) > 1:
                                for ele in valor_str.listTemp:
                                    if ele != -1:
                                        # ! Temporales aux
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        # ! Se genera código
                                        codigo += f"\t// IMPRIMIR \n" \
                                                  f"\t{tmp1} = S + {entorno.size};\n" \
                                                  f"\t{tmp2} = {tmp1} + 0;\n" \
                                                  f"\tSTACK[(int){tmp2}] = {ele};\n\n" \
                                                  f"\tS = S + {entorno.size};\n" \
                                                  f"\timprimir();\n" \
                                                  f"\tS = S - {entorno.size};\n"
                                    else:
                                        valor = valores.pop(0)
                                        # ! Validar el tipo de dato a formatear
                                        if valor.tipo[0] == TipoPrimitivo.I64:
                                            codigo += f"\t// EXPRESION\n" + valor.codigo + \
                                                      f"\t// IMPRIMIR \n" \
                                                      f"\tprintf(\"%d\", (int){valor.reference});\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.F64:
                                            codigo += f"\t// EXPRESION \n" + valor.codigo + \
                                                      f"\t// IMPRIMIR \n" \
                                                      f"\tprintf(\"%f\", {valor.reference});\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.CHAR:
                                            codigo += f"\t// EXPRESION \n" + valor.codigo + \
                                                      f"\t// IMPRIMIR\n" \
                                                      f"\tprintf(\"%c\", (int){valor.reference});\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.BOOL:
                                            lbl1 = generador.nuevoLabel()
                                            codigo += f"\t \n" + valor.codigo + \
                                                      f"\t{valor.trueLabel}:\n" \
                                                      f"\t \n" \
                                                      f"\tprintf(\"%c\", 116);\n" \
                                                      f"\tprintf(\"%c\", 114);\n" \
                                                      f"\tprintf(\"%c\", 117);\n" \
                                                      f"\tprintf(\"%c\", 101);\n" \
                                                      f"\tgoto {lbl1};\n" \
                                                      f"\t{valor.falseLabel}:\n" \
                                                      f"\t \n" \
                                                      f"\tprintf(\"%c\", 102);\n" \
                                                      f"\tprintf(\"%c\", 97);\n" \
                                                      f"\tprintf(\"%c\", 108);\n" \
                                                      f"\tprintf(\"%c\", 115);\n" \
                                                      f"\tprintf(\"%c\", 101);\n" \
                                                      f"\t{lbl1}:\n\n"

                                        elif valor.tipo[0] in [TipoPrimitivo.STR, TipoPrimitivo.STRING]:
                                            tmp1 = generador.nuevoTemp()
                                            tmp2 = generador.nuevoTemp()
                                            # ! Se genera código
                                            codigo += f"\t// IMPRIMIR EXPRESION \n" + valor.codigo + \
                                                      f"\t{tmp1} = S + {entorno.size};\n" \
                                                      f"\t{tmp2} = {tmp1} + 0;\n" \
                                                      f"\tSTACK[(int){tmp2}] = {valor.reference};\n\n" \
                                                      f"\tS = S + {entorno.size};\n" \
                                                      f"\timprimir();\n" \
                                                      f"\tS = S - {entorno.size};\n"

                                        else:
                                            # Generar código
                                            codigo += f"\t// EXPRESION \n" + valor.codigo + \
                                                      f"\t// IMPRIMIR \n"
                                            # Generar código de impresión de array
                                            codigo = self.imprimir_arreglo_vector(generador, entorno, codigo, valor.reference, valor.tipo)
                            else:
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                # ! Se genera código
                                codigo += f"\t// IMPRIMIR CADENA \n" \
                                          f"\t{tmp1} = S + {entorno.size};\n" \
                                          f"\t{tmp2} = {tmp1} + 0;\n" \
                                          f"\tSTACK[(int){tmp2}] = {valor_str.reference};\n\n" \
                                          f"\tS = S + {entorno.size};\n" \
                                          f"\timprimir();\n" \
                                          f"\tS = S - {entorno.size};\n"

                            codigo += f"\tprintf(\"%c\", 10);\n"
                            if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
                                # ! Obtener etiqueta de salida
                                lbl1 = generador.nuevoLabel()
                                # ! Reemplazar etiquetas
                                codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
                                # ! Agregar etiqueta al final
                                codigo += f"\t{lbl1}:\n"

                            return codigo
                        else:
                            alert = "Error en las expresiones el IMPRIMIR"
                            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                    else:
                        alert = "La cantidad de expreisones no coincide con la cantidad formateada"
                        List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                else:
                    alert = "Se esperaba un dato de tipo '&STR'"
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            else:
                alert = "Error en la expresion."
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

    def imprimir_arreglo_vector(self, generador, env, code, tmp, tipo):
        # ! Validar el tipo de entrada
        if tipo[0] == TipoPrimitivo.I64:
            code += f"\tprintf(\"%d\", (int){tmp});\n"
        elif tipo[0] == TipoPrimitivo.F64:
            code += f"\tprintf(\"%f\", {tmp});\n"
        elif tipo[0] == TipoPrimitivo.CHAR:
            code += f"\tprintf(\"%c\", 39);\n" \
                    f"\tprintf(\"%c\", (int){tmp});\n" \
                    f"\tprintf(\"%c\", 39);\n\n"
        elif tipo[0] == TipoPrimitivo.BOOL:
            # ! Labels aux
            lbl1 = generador.nuevoLabel()
            lbl2 = generador.nuevoLabel()
            lbl3 = generador.nuevoLabel()
            # ! Se genera código
            code += f"\tif ({tmp}) goto {lbl1};\n" \
                    f"\tgoto {lbl2};\n" \
                    f"\t{lbl1}:\n" \
                    f"\tprintf(\"%c\", 116);\n" \
                    f"\tprintf(\"%c\", 114);\n" \
                    f"\tprintf(\"%c\", 117);\n" \
                    f"\tprintf(\"%c\", 101);\n" \
                    f"\tgoto {lbl3};\n" \
                    f"\t{lbl2}:\n" \
                    f"\tprintf(\"%c\", 102);\n" \
                    f"\tprintf(\"%c\", 97);\n" \
                    f"\tprintf(\"%c\", 108);\n" \
                    f"\tprintf(\"%c\", 115);\n" \
                    f"\tprintf(\"%c\", 101);\n" \
                    f"\t{lbl3}:\n\n"

        elif tipo[0] in [TipoPrimitivo.STR, TipoPrimitivo.STRING]:
            tmp1 = generador.nuevoTemp()
            tmp2 = generador.nuevoTemp()

            # ! Se genera código
            code += f"\t{tmp1} = S + {env.size};\n" \
                    f"\t{tmp2} = {tmp1} + 0;\n" \
                    f"\tSTACK[(int){tmp2}] = {tmp};\n\n" \
                    f"\t \n" \
                    f"\tS = S + {env.size};\n" \
                    f"\timprimir();\n" \
                    f"\tS = S - {env.size};\n\n"

        else:  # ! Es de tipo arreglo/vector
            if tipo[0] == TipoPrimitivo.ARREGLO:
                pointer = 1
            else:
                pointer = 2

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
            lbl4 = generador.nuevoLabel()
            lbl5 = generador.nuevoLabel()

            # ! Se genera code
            code += f"\t{tmp1} = 0; \n" \
                    f"\t{tmp2} = {tmp} + 0;\n" \
                    f"\t{tmp3} = HEAP[(int){tmp2}]; \n\n" \
                    f"\tprintf(\"%c\", 91); \n" \
                    f"\t{lbl3}:\n" \
                    f"\tif ({tmp1} < {tmp3}) goto {lbl1}; \n" \
                    f"\tgoto {lbl2};\n" \
                    f"\t{lbl1}:\n" \
                    f"\t{tmp4} = {tmp} + {pointer}; \n" \
                    f"\t{tmp5} = {tmp4} + {tmp1}; \n" \
                    f"\t{tmp6} = HEAP[(int){tmp5}]; \n\n"

            # ! Code interno
            if tipo[1:]:
                code = self.imprimir_arreglo_vector(generador, env, code, tmp6, tipo[1:])

            # ! Se genera code final
            code += f"\t \n" \
                    f"\t{tmp7} = {tmp3} - 1; \n" \
                    f"\tif ({tmp1} < {tmp7}) goto {lbl4}; \n" \
                    f"\tgoto {lbl5};\n" \
                    f"\t{lbl4}:\n" \
                    f"\tprintf(\"%c\", 44); \n" \
                    f"\tprintf(\"%c\", 32); \n" \
                    f"\t{lbl5}:\n\n" \
                    f"\t{tmp1} = {tmp1} + 1; \n" \
                    f"\tgoto {lbl3}; \n" \
                    f"\t{lbl2}:\n" \
                    f"\tprintf(\"%c\", 93); \n\n"

        return code
