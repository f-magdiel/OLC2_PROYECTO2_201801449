class Valor:
    def __init__(self, fila, valor, esTemp, tipo):
        self.fila = fila
        self.valor = valor
        self.esTemp = esTemp
        self.tipo = tipo
        self.isLabel = ""
        self.notLabel = ""

    def obtenerValor(self):
        return self.valor
