class Variable:
    def __init__(self, fila, id, mutable, tipo):
        self.fila = fila
        self.id = id
        self.mutable = mutable
        self.tipo = tipo
        self.posicion = None
