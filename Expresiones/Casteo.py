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
            # ! de i64
            if self.tipo == TipoPrimitivo.I64:
                # ! a i64,f64,bool,char
                if valor.tipo in [TipoPrimitivo.I64, TipoPrimitivo.F64, TipoPrimitivo.BOOL, TipoPrimitivo.CHAR]:
                    if valor.tipo == TipoPrimitivo.BOOL:
                        nuevo_valor = Valor(self.fila, self.tipo)
                        tmp = generador.nuevoTemp()
                        nuevo_valor.reference = tmp
                        nuevo_valor.codigo = valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                            f"\t{tmp} = 1;\n" \
                                                            f"\t{valor.falseLabel}:\n" \
                                                            f"\t{tmp} = 0;\n"
                        return nuevo_valor
                    else:
                        valor.tipo = self.tipo

                    return valor
                else:
                    print("Error")
            # ! de f64
            elif self.tipo == TipoPrimitivo.F64:
                # ! a i64,f64
                if valor.tipo in [TipoPrimitivo.F64, TipoPrimitivo.I64]:
                    valor.tipo = self.tipo
                    return valor
                else:
                    print("Error")
            # ! de bool
            elif self.tipo == TipoPrimitivo.BOOL:
                # ! a bool
                if valor.tipo == TipoPrimitivo.BOOL:
                    return valor
                else:
                    print("Error")
            # ! de char
            elif self.tipo == TipoPrimitivo.CHAR:
                # ! a i64, char
                if valor.tipo in [TipoPrimitivo.I64, TipoPrimitivo.CHAR]:
                    valor.tipo = self.tipo
                    return valor
                else:
                    print("Error")
            # ! de str
            elif self.tipo == TipoPrimitivo.STR:
                if valor.tipo == TipoPrimitivo.STR:
                    return valor
                else:
                    print("Error")
            # ! de string
            else:
                if valor.tipo == TipoPrimitivo.STRING:
                    return valor
                else:
                    print("Error")
        else:
            print("Error en expresion")
