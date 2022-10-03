from Abstracta.Instruccion import Instruccion
from Entorno.Entorno import Entorno


class Main(Instruccion):
    def __init__(self, fila, instrucciones):
        super().__init__(fila)
        self.instrucciones = instrucciones

    def convertir(self, generador, entorno):
        env = Entorno(entorno)
        for instr in self.instrucciones:
            codigo = instr.convertir(generador, env)
            generador.codigo.append(codigo)
