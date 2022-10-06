import time


class Errores:
    def __init__(self, fila, info, tipo):
        self.fila = fila
        self.info = info
        self.tipo = tipo
        self.tiempo = time.strftime("%d/%m/%y"), time.strftime("%H,%M")


# !--------------------------------------------------
Tabla_Errorres = []
Tabla_Simbolos = []
Tabla_Impresion = []
Envs = []
