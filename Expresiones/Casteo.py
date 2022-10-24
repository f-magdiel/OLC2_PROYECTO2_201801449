from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Casteo(Expresion):
    def __init__(self, fila, expresion, tipo):
        super().__init__(fila)
        self.expresion = expresion
        self.tipo = tipo

    def convertir(self, generador, entorno):
        valor = self.expresion.convertir(generador, entorno)
        if valor:

            # ! DE I64
            if self.tipo == TipoPrimitivo.I64:

                # ! a i64,f64,bool,char
                if valor.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.F64, TipoPrimitivo.BOOL, TipoPrimitivo.CHAR]:

                    nuevo_valor = Valor(self.fila, [self.tipo])
                    nuevo_valor.reference = generador.nuevoTemp()
                    if valor.tipo[0] == TipoPrimitivo.BOOL:
                        lbl1 = generador.nuevoLabel()
                        # ! Se genera codigo
                        nuevo_valor.codigo = valor.codigo + f"\t/* CASTEO */\n" \
                                                            f"\t{valor.trueLabel}:\n" \
                                                            f"\t{nuevo_valor.reference} = 1;\n" \
                                                            f"\tgoto {lbl1};\n" \
                                                            f"\t{nuevo_valor.falseLabel}:\n" \
                                                            f"\t{nuevo_valor.reference} = 0;\n" \
                                                            f"\t{lbl1}:\n"
                    else:
                        # ! Se genera códig
                        nuevo_valor.codigo = valor.codigo + f"\t/* CASTEO */\n" \
                                                            f"\t{nuevo_valor.reference} = (int){valor.reference};\n"

                    return nuevo_valor

                else:
                    print("Error")
            # ! DE F64
            elif self.tipo == TipoPrimitivo.F64:
                # ! a i64,f64
                if valor.tipo[0] in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    nuevo_valor = Valor(self.fila, [self.tipo])
                    nuevo_valor.reference = generador.nuevoTemp()
                    # ! Se genera código
                    nuevo_valor.codigo = valor.codigo + f"\t/* CASTEO */\n" \
                                                        f"\t{nuevo_valor.reference} = (float){valor.reference};\n"

                    return nuevo_valor
                else:
                    print("Error")
            # ! DE BOOL
            elif self.tipo == TipoPrimitivo.BOOL:
                # ! A BOOL
                if valor.tipo[0] == TipoPrimitivo.BOOL:
                    return valor
                else:
                    print("Error")
            # ! DE CHAR
            elif self.tipo == TipoPrimitivo.CHAR:
                # ! A I64, CHAR
                if valor.tipo[0] in [TipoPrimitivo.I64, TipoPrimitivo.CHAR]:
                    valor.tipo[0] = self.tipo
                    return valor
                else:
                    print("Error")
            # ! DE STR
            elif self.tipo == TipoPrimitivo.STR:
                if valor.tipo[0] == TipoPrimitivo.STR:
                    return valor
                else:
                    print("Error")
            # ! DE STRING
            else:
                if valor.tipo[0] == TipoPrimitivo.STRING:
                    return valor
                else:
                    print("Error")

        else:
            print("Error en expresion")
