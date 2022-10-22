from Enum.TipoPrimitivo import TipoPrimitivo


class ArrayTipo:
    def __init__(self, tipo, flag_arreglo=False):
        self.tipo = tipo
        self.flag_arreglo = flag_arreglo

    def obtener_tipo(self):
        if self.flag_arreglo:
            if not isinstance(self.tipo, ArrayTipo):
                return [TipoPrimitivo.ARREGLO, self.tipo]
            else:
                tipo = self.tipo.obtener_tipo()
                tipo.insert(0, TipoPrimitivo.ARREGLO)
                return tipo

        else:
            if not isinstance(self.tipo, ArrayTipo):
                return [TipoPrimitivo.VECTOR, self.tipo]
            else:
                tipo = self.tipo.obtener_tipo()
                tipo.insert(0, TipoPrimitivo.VECTOR)
                return tipo
