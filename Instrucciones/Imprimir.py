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
            print("EPXRES ", valor_str.listTemp)
            if valor_str:
                if valor_str.tipo == TipoPrimitivo.STR:
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
                            if valor_str.listTemp:
                                # codigo += f"\t/* IMPRIMIR */\n"
                                for ele in valor_str.listTemp:
                                    if ele != -1:
                                        tmp1 = generador.nuevoTemp()

                                        codigo += f"\tS = S + {entorno.size};\n" \
                                                  f"\t{tmp1} = S + 0;\n" \
                                                  f"\tSTACK[(int){tmp1}] = {ele};\n" \
                                                  f"\timprimir();\n" \
                                                  f"\tS = S - {entorno.size};\n"
                                    else:
                                        valor = valores.pop(0)
                                        if valor.tipo == TipoPrimitivo.I64:
                                            codigo += f"\tprintf(\"%d\", (int){valor.reference});\n"
                                        elif valor.tipo == TipoPrimitivo.F64:
                                            codigo += f"\tprintf(\"%f\", {valor.reference});\n"
                                        elif valor.tipo == TipoPrimitivo.CHAR:
                                            codigo += f"\tprintf(\"%c\", (int){valor.reference});\n"
                                        elif valor.tipo == TipoPrimitivo.BOOL:
                                            lbl1 = generador.nuevoLabel()
                                            codigo += valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                     f"\tprintf(\"%d\", 1);\n" \
                                                                     f"\tgoto {lbl1};\n" \
                                                                     f"\t{valor.falseLabel}:\n" \
                                                                     f"\tprintf(\"%d\", 0);\n" \
                                                                     f"\t{lbl1}:\n"
                                        elif valor.tipo == TipoPrimitivo.STR:
                                            tmp1 = generador.nuevoTemp()
                                            codigo += valor.codigo + f"\tS = S + {entorno.size};\n" \
                                                                     f"\t{tmp1} = S + 0;\n" \
                                                                     f"\tSTACK[(int){tmp1}] = {valor.reference};\n" \
                                                                     f"\timprimir();\n" \
                                                                     f"\tS = S - {entorno.size};\n"
                                        # TODO: arreglos y vectores
                            else:
                                tmp1 = generador.nuevoTemp()
                                codigo += f"\tS = S +{entorno.size};\n" \
                                          f"\t{tmp1} = S + 0;\n" \
                                          f"\tSTACK[(int){tmp1}] = {valor_str.reference};\n" \
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
