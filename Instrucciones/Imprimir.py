from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo


class Imprimir(Instruccion):
    def __init__(self, fila, expresiones):
        super().__init__(fila)
        self.expresiones = expresiones

    def convertir(self, generador, entorno):
        if not self.expresiones:
            codigo = f"\t/* IMPRIMIR */\n" \
                     f"\tprintf(\"%c\", 10);\n"
            return codigo
        else:
            valor_str = self.expresiones[0].convertir(generador, entorno)
            if valor_str:
                if valor_str.tipo[0] == TipoPrimitivo.STR:
                    if len(self.expresiones) - 1 == valor_str.listTemp.count(-1):
                        codigo = f"\t/* IMPRIMIR */\n" + valor_str.codigo
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
                                        codigo += f"\t/* IMPRIMIR SUBCADENA */\n" \
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
                                                      f"\t// IMPRIMIR EXPRESION\n" \
                                                      f"\tprintf(\"%d\", (int){valor.reference});\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.F64:
                                            codigo += f"\t// Expresión\n" + valor.codigo + \
                                                      f"\t// Imprimir expresión\n" \
                                                      f"\tprintf(\"%f\", {valor.reference});\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.CHAR:
                                            codigo += f"\t// Expresión\n" + valor.codigo + \
                                                      f"\t// Imprimir expresión\n" \
                                                      f"\tprintf(\"%c\", (int){valor.reference});\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.BOOL:
                                            lbl1 = generador.nuevoLabel()
                                            codigo += f"\t// Expresión\n" + valor.codigo + \
                                                      f"\t{valor.trueLabel}:\n" \
                                                      f"\t// Imprimir expresión\n" \
                                                      f"\tprintf(\"%d\", 1);\n" \
                                                      f"\tgoto {lbl1};\n" \
                                                      f"\t{valor.falseLabel}:\n" \
                                                      f"\t// Imprimir expresión\n" \
                                                      f"\tprintf(\"%d\", 0);\n" \
                                                      f"\t{lbl1}:\n\n"

                                        elif valor.tipo[0] == TipoPrimitivo.STR:
                                            tmp1 = generador.nuevoTemp()
                                            tmp2 = generador.nuevoTemp()
                                            # ! Se genera código
                                            codigo += f"\t/* IMPRIMIR EXPRESION */\n" + valor.codigo + \
                                                      f"\t{tmp1} = S + {entorno.size};\n" \
                                                      f"\t{tmp2} = {tmp1} + 0;\n" \
                                                      f"\tSTACK[(int){tmp2}] = {valor.reference};\n\n" \
                                                      f"\tS = S + {entorno.size};\n" \
                                                      f"\timprimir();\n" \
                                                      f"\tS = S - {entorno.size};\n"

                                        elif valor.tipo[0] == TipoPrimitivo.ARREGLO:
                                            codigo += f"\t// Expresión\n" + valor.codigo
                                            codigo = self.imprimir_arreglo(generador, entorno, codigo, valor.reference, valor.tipo)
                                        else:
                                            pass
                                            # TODO:  vectores falta
                            else:
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                # ! Se genera código
                                codigo += f"\t/* IMPRIMIR CADENA */\n" \
                                          f"\t{tmp1} = S + {entorno.size};\n" \
                                          f"\t{tmp2} = {tmp1} + 0;\n" \
                                          f"\tSTACK[(int){tmp2}] = {valor_str.reference};\n\n" \
                                          f"\tS = S + {entorno.size};\n" \
                                          f"\timprimir();\n" \
                                          f"\tS = S - {entorno.size};\n"

                            codigo += f"\tprintf(\"%c\", 10);\n"
                            return codigo
                        else:
                            print("Error")
                    else:
                        print("Error")
                else:
                    print("Error")
            else:
                print("Error")

    def imprimir_arreglo(self, generador, env, code, tmp, tipo):
        if tipo[0] == TipoPrimitivo.I64:
            code += f"\tprintf(\"%d\", (int){tmp});\n"
        elif tipo[0] == TipoPrimitivo.F64:
            code += f"\tprintf(\"%f\", {tmp});\n"
        elif tipo[0] == TipoPrimitivo.CHAR:
            code += f"\tprintf(\"%c\", (int){tmp});\n"
        elif tipo[0] == TipoPrimitivo.BOOL:
            code += f"\tprintf(\"%d\", {tmp});\n"
        elif tipo[0] == TipoPrimitivo.STR:
            tmp1 = generador.nuevoTemp()
            tmp2 = generador.nuevoTemp()

            # ! Se genera código
            code += f"\t{tmp1} = S + {env.size};\n" \
                    f"\t{tmp2} = {tmp1} + 0;\n" \
                    f"\tSTACK[(int){tmp2}] = {tmp};\n\n" \
                    f"\t// Imprimir expresión\n" \
                    f"\tS = S + {env.size};\n" \
                    f"\timprimir();\n" \
                    f"\tS = S - {env.size};\n\n"

        elif tipo[0] == TipoPrimitivo.ARREGLO:
            # ! Temporales aux
            tmp1 = generador.nuevoTemp()
            tmp2 = generador.nuevoTemp()
            tmp3 = generador.nuevoTemp()
            tmp4 = generador.nuevoTemp()
            tmp5 = generador.nuevoTemp()
            tmp6 = generador.nuevoTemp()

            # ! Labels aux
            lbl1 = generador.nuevoLabel()
            lbl2 = generador.nuevoLabel()
            lbl3 = generador.nuevoLabel()

            # ! Se genera code
            code += f"\t// Imprimir arreglo\n" \
                    f"\t{tmp1} = {tmp}; // Puntero arreglo\n" \
                    f"\t{tmp2} = 0; // i\n" \
                    f"\t{tmp3} = HEAP[(int){tmp1}]; // len\n" \
                    f"\tprintf(\"%c\", 91); // [\n\n" \
                    f"\t{lbl3}:\n" \
                    f"\tif ({tmp2} < {tmp3}) goto {lbl1}; // i < len\n" \
                    f"\tgoto {lbl2};\n" \
                    f"\t{lbl1}:\n" \
                    f"\t{tmp4} = {tmp1} + 1; // Puntero valores\n" \
                    f"\t{tmp5} = {tmp4} + {tmp2}; // Dir. valor\n" \
                    f"\t{tmp6} = HEAP[(int){tmp5}]; // Valor\n\n"

            # ! Code interno
            if tipo[1:]:
                code = self.imprimir_arreglo(generador, env, code, tmp6, tipo[1:])
                # ! Se genera code
            code += f"\t{tmp2} = {tmp2} + 1; // i++\n" \
                    f"\tgoto {lbl3}; // Sig. pos\n" \
                    f"\t{lbl2}:\n" \
                    f"\tprintf(\"%c\", 93); // ]\n\n"
        else:
            pass
            # TODO: Aqui es vec

        return code
