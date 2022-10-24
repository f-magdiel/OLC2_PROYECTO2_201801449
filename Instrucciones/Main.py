from Abstracta.Instruccion import Instruccion
from Entorno.Entorno import Entorno
from Reporte.Contenido import Envs


class Main(Instruccion):
    def __init__(self, fila, instrucciones):
        super().__init__(fila)
        self.instrucciones = instrucciones

    def convertir(self, generador, entorno):
        env_main = Entorno(entorno, entorno.flag_bucle)
        for instr in self.instrucciones:
            code = instr.convertir(generador, env_main)
            if code:
                generador.codigo.append(code + "\n")
