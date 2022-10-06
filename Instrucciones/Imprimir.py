from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo


class Imprimir(Instruccion):
    def __init__(self, fila,  expresiones):
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
                            if valor_str.listTemp:
                                for ele in valor_str.listTemp:
                                    if ele != -1:
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        # ! Se genera código
                                        codigo += f"\t/* IMPRIMIR CADENA */\n" \
                                                  f"\t{tmp1} = S + {entorno.size};\n" \
                                                  f"\t{tmp2} = {tmp1} + 0;\n" \
                                                  f"\tSTACK[(int){tmp2}] = {ele};\n\n" \
                                                  f"\tS = S + {entorno.size};\n" \
                                                  f"\timprimir();\n" \
                                                  f"\tS = S - {entorno.size};\n"
                                    else:
                                        valor = valores.pop(0)
                                        if valor.tipo[0] == TipoPrimitivo.I64:
                                            codigo += valor.codigo + f"\tprintf(\"%d\", (int){valor.reference});\n"
                                        elif valor.tipo[0] == TipoPrimitivo.F64:
                                            codigo += valor.codigo + f"\tprintf(\"%f\", {valor.reference});\n"
                                        elif valor.tipo[0] == TipoPrimitivo.CHAR:
                                            codigo += valor.codigo + f"\tprintf(\"%c\", (int){valor.reference});\n"
                                        elif valor.tipo[0] == TipoPrimitivo.BOOL:
                                            lbl1 = generador.nuevoLabel()
                                            codigo += valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                     f"\tprintf(\"%d\", 1);\n" \
                                                                     f"\tgoto {lbl1};\n" \
                                                                     f"\t{valor.falseLabel}:\n" \
                                                                     f"\tprintf(\"%d\", 0);\n" \
                                                                     f"\t{lbl1}:\n"

                                        elif valor.tipo[0] == TipoPrimitivo.STR:
                                            tmp1 = generador.nuevoTemp()
                                            tmp2 = generador.nuevoTemp()
                                            # ! Se genera código
                                            codigo += f"\t/* IMPRIMIR CADENA */\n" + valor.codigo + \
                                                      f"\t{tmp1} = S + {entorno.size};\n" \
                                                      f"\t{tmp2} = {tmp1} + 0;\n" \
                                                      f"\tSTACK[(int){tmp2}] = {valor.reference};\n\n" \
                                                      f"\tS = S + {entorno.size};\n" \
                                                      f"\timprimir();\n" \
                                                      f"\tS = S - {entorno.size};\n"
                                        # TODO: arreglos y vectores, falta
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
