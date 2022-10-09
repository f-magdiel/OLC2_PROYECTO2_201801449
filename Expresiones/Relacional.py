from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Relacional(Expresion):
    def __init__(self, fila, exp1, operador, exp2):
        super().__init__(fila)
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

    def convertir(self, generador, entorno):
        # ! Convertir las expres y obtener resultados operados
        val_izq = self.exp1.convertir(generador, entorno)
        val_der = self.exp2.convertir(generador, entorno)

        if val_izq and val_der:
            if val_izq.tipo[0] == val_der.tipo[0] and val_izq.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64, TipoPrimitivo.STR]:
                nuevo_valor = Valor(self.fila, [TipoPrimitivo.BOOL])
                if val_izq.tipo[0] != TipoPrimitivo.STR:
                    nuevo_valor.trueLabel = generador.nuevoLabel()
                    nuevo_valor.falseLabel = generador.nuevoLabel()

                    nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\tif ({val_izq.reference} {self.operador} {val_der.reference}) goto {nuevo_valor.trueLabel};\n" \
                                                                           f"\tgoto {nuevo_valor.falseLabel};\n"
                else:
                    # ! Temporales aux
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    tmp4 = generador.nuevoTemp()
                    tmp5 = generador.nuevoTemp()
                    tmp6 = generador.nuevoTemp()
                    tmp7 = generador.nuevoTemp()
                    tmp8 = generador.nuevoTemp()
                    # ! Labels aux
                    lbl1 = generador.nuevoLabel()
                    lbl2 = generador.nuevoLabel()
                    lbl3 = generador.nuevoLabel()
                    lbl4 = generador.nuevoLabel()
                    lbl5 = generador.nuevoLabel()
                    lbl6 = generador.nuevoLabel()

                    nuevo_valor.trueLabel = generador.nuevoLabel()
                    nuevo_valor.falseLabel = generador.nuevoLabel()
                    # ! Se genera código
                    nuevo_valor.codigo = val_izq.codigo + val_der.codigo + f"\t// Comparar cadenas\n" \
                                                                      f"\t{tmp1} = 0; // Contador1\n" \
                                                                      f"\t{tmp2} = 0; // Contador2\n\n" \
                                                                      f"\t{tmp3} = {val_izq.reference};\n" \
                                                                      f"\t{lbl3}: // Recorrer cadena1\n" \
                                                                      f"\t{tmp4} = HEAP[(int){tmp3}]; // char → cadena1\n" \
                                                                      f"\t{tmp5} = - 1;\n" \
                                                                      f"\tif ({tmp4} != {tmp5}) goto {lbl1}; // Fin de cadena1?\n" \
                                                                      f"\tgoto {lbl2};\n" \
                                                                      f"\t{lbl1}:\n" \
                                                                      f"\t{tmp3} = {tmp3} + 1;\n" \
                                                                      f"\t{tmp1} = {tmp1} + 1; // Contador1++\n" \
                                                                      f"\tgoto {lbl3};\n" \
                                                                      f"\t{lbl2}:\n\n" \
                                                                      f"\t{tmp6} = {val_der.reference};\n" \
                                                                      f"\t{lbl6}: // Recorrer cadena2\n" \
                                                                      f"\t{tmp7} = HEAP[(int){tmp6}]; // char → cadena2\n" \
                                                                      f"\t{tmp8} = - 1;\n" \
                                                                      f"\tif ({tmp7} != {tmp8}) goto {lbl4}; // Fin de cadena2?\n" \
                                                                      f"\tgoto {lbl5};\n" \
                                                                      f"\t{lbl4}:\n" \
                                                                      f"\t{tmp6} = {tmp6} + 1;\n" \
                                                                      f"\t{tmp2} = {tmp2} + 1; // Contador2++\n" \
                                                                      f"\tgoto {lbl6};\n" \
                                                                      f"\t{lbl5}:\n\n" \
                                                                      f"\tif ({tmp1} {self.operador} {tmp2}) goto {nuevo_valor.trueLabel};\n" \
                                                                      f"\tgoto {nuevo_valor.falseLabel};\n"
                return nuevo_valor
            else:
                print("Error expresiones incompatibles")
        else:
            print("Error en expresiones")
