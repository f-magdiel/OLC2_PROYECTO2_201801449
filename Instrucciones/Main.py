from Abstracta.Instruccion import Instruccion
from Entorno.Entorno import Entorno
from Reporte.Contenido import Envs
from General.General import Env_General

class Main(Instruccion):
    def __init__(self, fila, instrucciones):
        super().__init__(fila)
        self.instrucciones = instrucciones

    def convertir(self, generador, entorno):
        env_main = Entorno(entorno, entorno.flag_bucle)
        Env_General.append(env_main)
        for instr in self.instrucciones:
            code = instr.convertir(generador, env_main)
            if code:
                generador.codigo.append(code + "\n")
