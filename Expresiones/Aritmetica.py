from Abstracta.Expresion import Expresion
from Enum.OpAritmetico import OPERADOR_ARITMETICO
from Entorno.Entorno import Entorno
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Aritmetica(Expresion):
    def __init__(self, fila, exp1, operador, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def convertir(self, entorno: Entorno):
        self.exp1.generador = self.generador
        self.exp2.generador = self.generador
        val_izq = self.exp1.convertir(entorno)
        val_der = self.exp2.convertir(entorno)

        if self.exp1 and self.exp2:
            # ! SUMA
            if val_izq and val_der:
                if self.operador == OPERADOR_ARITMETICO.MAS:
                    # ! suma de i64, f64
                    if val_izq.tipo == val_der.tipo and val_izq.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        # ! valor a retornar
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        # ! generar tempora
                        tmp = self.generador
                        nuevo_valor.reference = tmp
                        # ! generar c3d
                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{tmp} = {val_izq.reference} + {val_der.reference};\n"
                        return nuevo_valor

                    elif val_izq.tipo in [TipoPrimitivo.TOS, TipoPrimitivo.TOW] and val_der.tipo == TipoPrimitivo.STR:
                        # ! valor a retornar
                        nuevo_valor = Valor(self.fila, TipoPrimitivo.STR)
                        tmp1 = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp1

                        tmp2 = self.generador.nuevoTemp()
                        tmp3 = self.generador.nuevoTemp()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{tmp1} = HP;\n" \
                                                                               f"\tSP = SP + {entorno.size};\n" \
                                                                               f"\t{tmp2} = SP + 0;\n" \
                                                                               f"\tSTACK[(int){tmp2}] = {val_izq.reference};\n" \
                                                                               f"\t{tmp3} = SP + 1;\n" \
                                                                               f"\tSTACK[(int){tmp3}] = {val_der.reference};\n" \
                                                                               f"\tconcatenar();\n" \
                                                                               f"\tSP = SP - {entorno.size};\n"

                        return nuevo_valor
                    else:
                        print("Error")
                # ! RESTA
                elif self.operador == OPERADOR_ARITMETICO.MENOS:
                    # ! resta para i64, f64
                    if val_izq.tipo == val_der.tipo and val_der.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        tmp = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{tmp} = {val_izq.reference} - {val_der.reference};\n"
                        return nuevo_valor
                    else:
                        print("Error")

                # ! Mutiplicación
                elif self.operador == OPERADOR_ARITMETICO.POR:
                    # ! multiplicación para i64, f64
                    if val_izq.tipo == val_der.tipo and val_izq.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        tmp = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp
                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t{tmp} = {val_izq.reference} * {val_der.reference};\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! División
                elif self.operador == OPERADOR_ARITMETICO.DIVIDIDO:
                    # ! división para f64, i64
                    if val_izq.tipo == val_der.tipo and val_izq.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, TipoPrimitivo.F64)
                        tmp = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp

                        # ! label aux
                        lbl1 = self.generador.nuevoLabel()
                        lbl2 = self.generador.nuevoLabel()
                        lbl3 = self.generador.nuevoLabel()

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
                                                                               f"\t{tmp} = 0;\n" \
                                                                               f"\tgoto {lbl3};\n" \
                                                                               f"\t{lbl2}:\n" \
                                                                               f"\t{tmp} = {val_izq.reference} / {val_der.reference};\n" \
                                                                               f"\t{lbl3}:\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! Potencia
                elif self.operador == OPERADOR_ARITMETICO.POTENCIA:
                    if val_izq.tipo == TipoPrimitivo.I64 and val_der.tipo == TipoPrimitivo.I64:
                        nuevo_valor = Valor(self.fila, TipoPrimitivo.I64)
                        tmp = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp

                        tmp1 = self.generador.nuevoTemp()

                        lbl1 = self.generador.nuevoLabel()
                        lbl2 = self.generador.nuevoLabel()
                        lbl3 = self.generador.nuevoLabel()
                        lbl4 = self.generador.nuevoLabel()
                        lbl5 = self.generador.nuevoLabel()
                        lbl6 = self.generador.nuevoLabel()
                        lbl7 = self.generador.nuevoLabel()
                        lbl8 = self.generador.nuevoLabel()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.reference} != 0) goto {lbl1};\n" \
                                                                               f"\tgoto {lbl2};\n" \
                                                                               f"\t{lbl1}:\n" \
                                                                               f"\tif ({val_der.reference} != 1) goto {lbl6};\n" \
                                                                               f"\tgoto {lbl7};\n" \
                                                                               f"\t{lbl6}: // for\n" \
                                                                               f"\t{tmp} = 1; // Valor inicial\n" \
                                                                               f"\t{tmp1} = 0; // Contador\n" \
                                                                               f"\t{lbl5}:\n" \
                                                                               f"\tif ({tmp1} < {val_der.reference}) goto {lbl3};\n" \
                                                                               f"\tgoto {lbl4};\n" \
                                                                               f"\t{lbl3}:\n" \
                                                                               f"\t{tmp} = {tmp} * {val_izq.reference};\n" \
                                                                               f"\t{tmp1} = {tmp1} + 1;\n" \
                                                                               f"\tgoto {lbl5};\n" \
                                                                               f"\t{lbl4}:\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl7}: // retornar el mismo\n" \
                                                                               f"\t{tmp} = {val_izq.reference};\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl2}: // Retornar 1\n" \
                                                                               f"\t{tmp} = 1;\n" \
                                                                               f"\t{lbl8}:\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! Potencia f
                elif self.operador == OPERADOR_ARITMETICO.POTENCIAF:
                    if val_izq.tipo == TipoPrimitivo.F64 and val_der.tipo == TipoPrimitivo.F64:
                        nuevo_valor = Valor(self.fila, TipoPrimitivo.F64)
                        tmp = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp

                        tmp1 = self.generador.nuevoTemp()

                        # ! labels aux
                        lbl1 = self.generador.nuevoLabel()
                        lbl2 = self.generador.nuevoLabel()
                        lbl3 = self.generador.nuevoLabel()
                        lbl4 = self.generador.nuevoLabel()
                        lbl5 = self.generador.nuevoLabel()
                        lbl6 = self.generador.nuevoLabel()
                        lbl7 = self.generador.nuevoLabel()
                        lbl8 = self.generador.nuevoLabel()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.reference} != 0) goto {lbl1};\n" \
                                                                               f"\tgoto {lbl2};\n" \
                                                                               f"\t{lbl1}:\n" \
                                                                               f"\tif ({val_der.reference} != 1) goto {lbl6};\n" \
                                                                               f"\tgoto {lbl7};\n" \
                                                                               f"\t{lbl6}: // for\n" \
                                                                               f"\t{tmp} = 1; // Valor inicial\n" \
                                                                               f"\t{tmp1} = 0; // Contador\n" \
                                                                               f"\t{lbl5}:\n" \
                                                                               f"\tif ({tmp1} < {val_der.reference}) goto {lbl3};\n" \
                                                                               f"\tgoto {lbl4};\n" \
                                                                               f"\t{lbl3}:\n" \
                                                                               f"\t{tmp} = {tmp} * {val_izq.ref};\n" \
                                                                               f"\t{tmp1} = {tmp1} + 1;\n" \
                                                                               f"\tgoto {lbl5};\n" \
                                                                               f"\t{lbl4}:\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl7}: // Retornar el mismo\n" \
                                                                               f"\t{tmp} = {val_izq.ref};\n" \
                                                                               f"\tgoto {lbl8}; // Fin\n" \
                                                                               f"\t{lbl2}: // Retornar 1\n" \
                                                                               f"\t{tmp} = 1;\n" \
                                                                               f"\t{lbl8}:\n"
                        return nuevo_valor
                    else:
                        print("Error")
                # ! Modulo
                else:

                    if val_izq.tipo == val_der.tipo and val_izq.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64]:
                        nuevo_valor = Valor(self.fila, val_izq.tipo)
                        tmp = self.generador.nuevoTemp()
                        nuevo_valor.reference = tmp

                        # ! labels aux
                        lbl1 = self.generador.nuevoLabel()
                        lbl2 = self.generador.nuevoLabel()
                        lbl3 = self.generador.nuevoLabel()

                        nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_der.ref} == 0) goto {lbl1};\n" \
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
                                                                               f"\t{tmp} = 0;\n" \
                                                                               f"\tgoto {lbl3};\n" \
                                                                               f"\t{lbl2}:\n" \
                                                                               f"\t{tmp} = {val_izq.reference} % {val_der.reference};\n" \
                                                                               f"\t{lbl3}:\n"
                        return nuevo_valor
                    else:
                        print("error")
            else:
                print("error de expresion")
