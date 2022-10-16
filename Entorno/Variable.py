class Variable:
    def __init__(self, fila, id, mutable, tipo, flag_reference=False):
        self.fila = fila
        self.id = id
        self.mutable = mutable
        self.tipo = tipo
        self.posicion = None
        self.flag_reference = flag_reference
