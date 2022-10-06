from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from General.General import List_Errores
from General.General import Env_General
from Instrucciones.Imprimir import Imprimir
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.If import If

class While(Instruccion):
    def __init__(self, fila, expresion, instrucciones):
        super().__init__(fila)
        self.expresion = expresion
        self.instrucciones = instrucciones

    def convertir(self, generador, entorno):
        # ! Convertir expresion
        nuevo_valor = self.expresion.convertir(generador, entorno)
        # ! Validar nuevo_valor
        if nuevo_valor:
            if nuevo_valor.tipo[0] == TipoPrimitivo.BOOL:
                env_while = Entorno(entorno, flag_bucle=True)
                Env_General.append(env_while)

                codigo = f"\t// Condición\n" + nuevo_valor.codigo + \
                         f"\t{nuevo_valor.trueLabel}:\n"
                # ! Temporal aux
                tmp1 = generador.nuevoTemp()
                # ! Se genera código para cambio entorno
                codigo += f"\t// Cambio de ámbito\n" \
                          f"\tS = S + {entorno.size};\n\n"
                # ! Recorrer instrucciones
                for instruc in self.instrucciones:
                    print("INSTRUCC",instruc)
                    if isinstance(instruc, Imprimir):
                        codigo += instruc.convertir(generador, env_while)
                    elif isinstance(instruc, Break):
                        codigo += instruc.convertir(generador, env_while)
                    elif isinstance(instruc, Continue):
                        codigo += instruc.convertir(generador, env_while)
                    elif isinstance(instruc, If):
                        codigo += instruc.convertir(generador, env_while)
                    else:
                        print("Error invalido en entorno")

                # ! Generar código de cambio de entorno
                codigo += f"\t// Cambio de ámbito\n" \
                          f"\tS = S - {entorno.size};\n\n"
                # ! Generar salto para repetir
                codigo += f"\tgoto ETIQUETA_WHILE;\n"
                # ! Colocar etiqueta falsa
                codigo += f"\t{nuevo_valor.falseLabel}:\n"
                # ! Obtener etiqueta de bucle
                lbl1 = generador.nuevoLabel()
                # ! Remplazar etiquetas
                codigo = codigo.replace("ETIQUETA_WHILE", lbl1)
                # ! Agregar etiqueta de while al inicio
                codigo = f"\t/* SENTENCIA WHILE */\n" \
                         f"\t{lbl1}:\n" + codigo

                if codigo.count("ETIQUETA_CONTINUE") > 0:
                    codigo = codigo.replace("TEMPORAL_CONTINUE", tmp1)
                    codigo = codigo.replace("ETIQUETA_CONTINUE", lbl1)

                if codigo.count("ETIQUETA_BREAK") > 0:
                    # ! Obtener etiqueta de salida
                    lbl2 = generador.nuevoLabel()
                    # ! Reemplazar etiquetas
                    codigo = codigo.replace("TEMPORAL_BREAK", tmp1)
                    codigo = codigo.replace("ETIQUETA_BREAK", lbl2)
                    # ! Agregar etiqueta al final
                    codigo += f"\t{lbl2}:\n"

                return codigo
            else:
                print("Error no es tipo bOol")
        else:
            print("Error en la condicion")
