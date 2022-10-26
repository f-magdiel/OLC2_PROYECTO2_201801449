from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR

class VectorUnico(Expresion):
    def __init__(self, fila, expresion=None):
        super().__init__(fila)
        self.expresion = expresion

    def convertir(self, generador, entorno):
        if self.expresion is None:
            valor = Valor(self.fila, [TipoPrimitivo.VECTOR])
            valor.reference = generador.nuevoTemp()
            # ! Temporales aux
            tmp1 = generador.nuevoTemp()
            tmp2 = generador.nuevoTemp()
            # ! Se genera código
            valor.codigo += f"\t// NEW VECTOR \n" \
                            f"\t{valor.reference} = H; \n" \
                            f"\tH = H + 2; \n" \
                            f"\t{tmp1} = {valor.reference} + 0;\n" \
                            f"\tHEAP[(int){tmp1}] = 0; \n" \
                            f"\t{tmp2} = {valor.reference} + 1;\n" \
                            f"\tHEAP[(int){tmp2}] = 1; \n\n"

            return valor
        else:
            valor_cap = self.expresion.convertir(generador, entorno)
            if valor_cap:
                if valor_cap.tipo[0] == TipoPrimitivo.I64:
                    valor = Valor(self.fila, [TipoPrimitivo.VECTOR])
                    valor.reference = generador.nuevoTemp()
                    # ! Temporales aux
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # ! Se genera código
                    valor.codigo += f"\t// WITH CAPACITY \n" \
                                    f"\t{valor.reference} = H; \n" \
                                    f"\tH = H + 2; \n" \
                                    f"\t{tmp1} = {valor.reference} + 0;\n" \
                                    f"\tHEAP[(int){tmp1}] = 0; \n\n" \
                                    f"\t \n" + valor_cap.codigo + \
                                    f"\t{tmp2} = {valor.reference} + 1;\n" \
                                    f"\tHEAP[(int){tmp2}] = {valor_cap.reference}; \n\n"
                    return valor
                else:
                    alert = "Error tipos incompatibles en VECTOR"
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            else:
                alert = "Error en expresiones en VECTOR"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
