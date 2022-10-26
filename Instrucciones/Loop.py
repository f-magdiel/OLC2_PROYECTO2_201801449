from Abstracta.Instruccion import Instruccion
from Entorno.Entorno import Entorno
from General.General import Env_General
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Imprimir import Imprimir
from Instrucciones.If import If
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Loop(Instruccion):
    def __init__(self, fila, instrucciones):
        super().__init__(fila)
        self.instrucciones = instrucciones

    def convertir(self, generador, entorno):
        env_loop = Entorno(generador, flag_bucle=True)
        Env_General.append(env_loop)

        codigo = ""

        for instruc in self.instrucciones:
            if isinstance(instruc, Break) and not env_loop.flag_bucle:
                alert = "Error en entorno de LOOP, instruccion no aceptable"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            elif isinstance(instruc, Continue) and not env_loop.flag_bucle:
                alert = "Error en entorno de LOOP, instruccion no aceptable"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            else:
                code = instruc.convertir(generador, env_loop)
                if code:
                    codigo += code + "\n"

        codigo = f"\t \n" \
                 f"\tS = S + {entorno.size};\n\n" + codigo + \
                 f"\t \n" \
                 f"\tS = S - {entorno.size};\n\n"

        tmp1 = generador.nuevoTemp()
        codigo = f"\t \n" \
                 f"\t{tmp1} = S;\n" + codigo

        lbl1 = generador.nuevoLabel()
        codigo = f"\t// LOOP \n" \
                 f"\t{lbl1}:\n" + codigo + \
                 f"\tgoto {lbl1}; \n"

        if codigo.count("ETIQUETA_CONTINUE") > 0:
            # Reemplazar etiquetas
            codigo = codigo.replace("TEMPORAL_CONTINUE", tmp1)
            codigo = codigo.replace("ETIQUETA_CONTINUE", lbl1)

        if codigo.count("ETIQUETA_BREAK") > 0:
            # Obtener etiqueta de salida
            lbl2 = generador.nuevoLabel()
            # Reemplazar etiquetas
            codigo = codigo.replace("TEMPORAL_BREAK", tmp1)
            codigo = codigo.replace("ETIQUETA_BREAK", lbl2)
            # Agregar etiqueta al final
            codigo += f"\t{lbl2}:\n"

        if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
            # ! Obtener etiqueta de salida
            lbl1 = generador.nuevoLabel()
            # ! Reemplazar etiquetas
            codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
            # ! Agregar etiqueta al final
            codigo += f"\t{lbl1}:\n"

        return codigo
