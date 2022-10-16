from Abstracta.Expresion import Expresion
from Enum.OpAritmetico import OPERADOR_ARITMETICO
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Aritmetica(Expresion):
    def __init__(self, fila, exp1, operador, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def convertir(self, generador, entorno):
        val_izq = self.exp1.convertir(generador, entorno)
        val_der = self.exp2.convertir(generador, entorno)

        if self.exp1 and self.exp2:
            # ! SUMA
            if val_izq and val_der:
                # ! MAS
                if self.operador == OPERADOR_ARITMETICO.MAS:
                    # ! suma de i64, f64
                    if val_izq.tipo[0] == val_der.tipo[0] and val_izq.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        # ! valor a retornar
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        # ! generar temporal
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! generar c3d
                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{nuevo_valor.reference} = {val_izq.reference} + {val_der.reference};\n"
                        return nuevo_valor
                    # ! STRIGN + STR
                    elif val_izq.tipo[0] == TipoPrimitivo.STRING and val_der.tipo[0] == TipoPrimitivo.STR:
                        # ! valor a retornar
                        nuevo_valor = Valor(self.fila, [TipoPrimitivo.STR])
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! Temp auxiliares
                        tmp1 = generador.nuevoTemp()
                        tmp2 = generador.nuevoTemp()
                        tmp3 = generador.nuevoTemp()
                        tmp4 = generador.nuevoTemp()
                        # ! Se genera código
                        nuevo_valor.codigo = f"\t/* CONCATENAR */\n" + val_izq.codigo + \
                                             f"\t{tmp1} = S + {entorno.size};\n" \
                                             f"\t{tmp2} = {tmp1} + 0;\n" \
                                             f"\tSTACK[(int){tmp2}] = {val_izq.reference};\n\n" + val_der.codigo + \
                                             f"\t{tmp3} = S + {entorno.size};\n" \
                                             f"\t{tmp4} = {tmp3} + 1;\n" \
                                             f"\tSTACK[(int){tmp4}] = {val_der.reference};\n\n" \
                                             f"\t{nuevo_valor.reference} = H;\n" \
                                             f"\tS = S + {entorno.size};\n" \
                                             f"\tconcatenar();\n" \
                                             f"\tS = S - {entorno.size};\n"

                        return nuevo_valor
                    else:
                        print("Error")
                # ! RESTA
                elif self.operador == OPERADOR_ARITMETICO.MENOS:
                    # ! resta para i64, f64
                    if val_izq.tipo[0] == val_der.tipo[0] and val_der.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! Se genera código
                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{nuevo_valor.reference} = {val_izq.reference} - {val_der.reference};\n"
                        return nuevo_valor
                    else:
                        print("Error")

                # ! MULTIPLICACIÓN
                elif self.operador == OPERADOR_ARITMETICO.POR:
                    # ! multiplicación para i64, f64
                    if val_izq.tipo[0] == val_der.tipo[0] and val_izq.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! Se genera código
                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{nuevo_valor.reference} = {val_izq.reference} * {val_der.reference};\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! DIVISIÓN
                elif self.operador == OPERADOR_ARITMETICO.DIVIDIDO:
                    # ! división para f64, i64
                    if val_izq.tipo[0] == val_der.tipo[0] and val_izq.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, [TipoPrimitivo.F64])
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! Labels temporales
                        lbl1 = generador.nuevoLabel()
                        lbl2 = generador.nuevoLabel()
                        lbl3 = generador.nuevoLabel()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.reference} == 0) goto {lbl1};\n" \
                                                                               f"\tgoto {lbl2};\n" \
                                                                               f"\t{lbl1}:\n" \
                                                                               f"\tprintf(\"%c\", 77); //M\n" \
                                                                               f"\tprintf(\"%c\", 97); //a\n" \
                                                                               f"\tprintf(\"%c\", 116); //t\n" \
                                                                               f"\tprintf(\"%c\", 104); //h\n" \
                                                                               f"\tprintf(\"%c\", 69); //E\n" \
                                                                               f"\tprintf(\"%c\", 114); //r\n" \
                                                                               f"\tprintf(\"%c\", 114); //r\n" \
                                                                               f"\tprintf(\"%c\", 111); //o\n" \
                                                                               f"\tprintf(\"%c\", 114); //r\n" \
                                                                               f"\t{nuevo_valor.reference} = 0;\n" \
                                                                               f"\tgoto {lbl3};\n" \
                                                                               f"\t{lbl2}:\n" \
                                                                               f"\t{nuevo_valor.reference} = (float){val_izq.reference} / (float){val_der.reference};\n" \
                                                                               f"\t{lbl3}:\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! POTENCIA
                elif self.operador == OPERADOR_ARITMETICO.POTENCIA:
                    if val_izq.tipo[0] == TipoPrimitivo.I64 and val_der.tipo[0] == TipoPrimitivo.I64:
                        nuevo_valor = Valor(self.fila, [TipoPrimitivo.I64])
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! Temporal nuevo_valor.reference
                        tmp1 = generador.nuevoTemp()
                        # ! Labels auxiliares
                        lbl1 = generador.nuevoLabel()
                        lbl2 = generador.nuevoLabel()
                        lbl3 = generador.nuevoLabel()
                        lbl4 = generador.nuevoLabel()
                        lbl5 = generador.nuevoLabel()
                        lbl6 = generador.nuevoLabel()
                        lbl7 = generador.nuevoLabel()
                        lbl8 = generador.nuevoLabel()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.reference} != 0) goto {lbl1};\n" \
                                                                               f"\tgoto {lbl2};\n" \
                                                                               f"\t{lbl1}:\n" \
                                                                               f"\tif ({val_der.reference} != 1) goto {lbl6};\n" \
                                                                               f"\tgoto {lbl7};\n" \
                                                                               f"\t{lbl6}: // for\n" \
                                                                               f"\t{nuevo_valor.reference} = 1; // Valor inicial\n" \
                                                                               f"\t{tmp1} = 0; // Contador\n" \
                                                                               f"\t{lbl5}:\n" \
                                                                               f"\tif ({tmp1} < {val_der.reference}) goto {lbl3};\n" \
                                                                               f"\tgoto {lbl4};\n" \
                                                                               f"\t{lbl3}:\n" \
                                                                               f"\t{nuevo_valor.reference} = {nuevo_valor.reference} * {val_izq.reference};\n" \
                                                                               f"\t{tmp1} = {tmp1} + 1;\n" \
                                                                               f"\tgoto {lbl5};\n" \
                                                                               f"\t{lbl4}:\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl7}: // retornar el mismo\n" \
                                                                               f"\t{nuevo_valor.reference} = {val_izq.reference};\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl2}: // Retornar 1\n" \
                                                                               f"\t{nuevo_valor.reference} = 1;\n" \
                                                                               f"\t{lbl8}:\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! POTENCIAF
                elif self.operador == OPERADOR_ARITMETICO.POTENCIAF:
                    if val_izq.tipo[0] == TipoPrimitivo.F64 and val_der.tipo[0] == TipoPrimitivo.F64:
                        nuevo_valor = Valor(self.fila, [TipoPrimitivo.F64])
                        nuevo_valor.reference = generador.nuevoTemp()
                        # ! Temporal aux
                        tmp1 = generador.nuevoTemp()

                        # nuevo_valor.referenceabels aux
                        lbl1 = generador.nuevoLabel()
                        lbl2 = generador.nuevoLabel()
                        lbl3 = generador.nuevoLabel()
                        lbl4 = generador.nuevoLabel()
                        lbl5 = generador.nuevoLabel()
                        lbl6 = generador.nuevoLabel()
                        lbl7 = generador.nuevoLabel()
                        lbl8 = generador.nuevoLabel()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.reference} != 0) goto {lbl1};\n" \
                                                                               f"\tgoto {lbl2};\n" \
                                                                               f"\t{lbl1}:\n" \
                                                                               f"\tif ({val_der.reference} != 1) goto {lbl6};\n" \
                                                                               f"\tgoto {lbl7};\n" \
                                                                               f"\t{lbl6}: // for\n" \
                                                                               f"\t{nuevo_valor.reference} = 1; // Valor inicial\n" \
                                                                               f"\t{tmp1} = 0; // Contador\n" \
                                                                               f"\t{lbl5}:\n" \
                                                                               f"\tif ({tmp1} < {val_der.reference}) goto {lbl3};\n" \
                                                                               f"\tgoto {lbl4};\n" \
                                                                               f"\t{lbl3}:\n" \
                                                                               f"\t{nuevo_valor.reference} = {nuevo_valor.reference} * {val_izq.reference};\n" \
                                                                               f"\t{tmp1} = {tmp1} + 1;\n" \
                                                                               f"\tgoto {lbl5};\n" \
                                                                               f"\t{lbl4}:\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl7}: // Retornar el mismo\n" \
                                                                               f"\t{nuevo_valor.reference} = {val_izq.reference};\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl2}: // Retornar 1\n" \
                                                                               f"\t{nuevo_valor.reference} = 1;\n" \
                                                                               f"\t{lbl8}:\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! MODULO
                else:
                    if val_izq.tipo[0] == val_der.tipo[0] and val_izq.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        nuevo_valor.reference = generador.nuevoTemp()

                        # ! labels aux
                        lbl1 = generador.nuevoLabel()
                        lbl2 = generador.nuevoLabel()
                        lbl3 = generador.nuevoLabel()
                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.reference} == 0) goto {lbl1};\n" \
                                                                               f"\tgoto {lbl2};\n" \
                                                                               f"\t{lbl1}:\n" \
                                                                               f"\tprintf(\"%c\", 77); //M\n" \
                                                                               f"\tprintf(\"%c\", 97); //a\n" \
                                                                               f"\tprintf(\"%c\", 116); //t\n" \
                                                                               f"\tprintf(\"%c\", 104); //h\n" \
                                                                               f"\tprintf(\"%c\", 69); //E\n" \
                                                                               f"\tprintf(\"%c\", 114); //r\n" \
                                                                               f"\tprintf(\"%c\", 114); //r\n" \
                                                                               f"\tprintf(\"%c\", 111); //o\n" \
                                                                               f"\tprintf(\"%c\", 114); //r\n" \
                                                                               f"\t{nuevo_valor.reference} = 0;\n" \
                                                                               f"\tgoto {lbl3};\n" \
                                                                               f"\t{lbl2}:\n" \
                                                                               f"\t{nuevo_valor.reference} = (int){val_izq.reference} % (int){val_der.reference};\n" \
                                                                               f"\t{lbl3}:\n"
                        return nuevo_valor
                    else:
                        print("error")
            else:
                print("error de expresion")
