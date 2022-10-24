from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo


class LlamadaFuncion(Instruccion):
    def __init__(self, fila, id, argumentos):
        super().__init__(fila)
        self.id = id
        self.argumentos = argumentos


    def convertir(self, generador, entorno):
        # ! Validar si existe la función en la tabla de símbolos

        if entorno.existe_fun(self.id, False):
            # ! Obtener la función
            funcion = entorno.obtener_fun(self.id)
            # ! Validar que la cantidad de parámetros y argumentos sean iguales
            if len(funcion.parametros) == len(self.argumentos):
                # ! Recorrer los argumentos, traducir y obtener los datos
                valores = []
                for i in range(len(self.argumentos)):
                    valores.append(self.argumentos[i].convertir(generador, entorno))
                # ! Validar que ningún dato sea None
                if None not in valores:
                    # ! Temporal de entorno pivote
                    tmp = generador.nuevoTemp()
                    # ! Crear código a retornar
                    codigo = f"\t/* LLAMADA A FUNCIÓN */\n" \
                             f"\t{tmp} = S + {entorno.size}; // Entorno simulado\n\n"
                    # ! Recorrer los datos de los argumentos
                    for i in range(len(valores)):
                        # ! Verificar el tipo
                        if valores[i].tipo[0] != TipoPrimitivo.BOOL:
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            # ! Generar código
                            codigo += f"\t// Argumento\n" + valores[i].codigo + \
                                      f"\t{tmp1} = {tmp} + {i + 1}; // Dir. param{i + 1}\n" \
                                      f"\tSTACK[(int){tmp1}] = {valores[i].reference}; // Asignar valor\n\n"
                        else:
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            # ! Etiquetas auxiliares
                            lbl1 = generador.nuevoLabel()
                            # ! Generar código
                            codigo += f"\t// Argumento\n" + valores[i].codigo + \
                                      f"\t{valores[i].trueLabel}:\n" \
                                      f"\t{tmp1} = {tmp} + {i + 1}; // Dir. param{i + 1}\n" \
                                      f"\tSTACK[(int){tmp1}] = 1; // Asignar valor\n" \
                                      f"\tgoto {lbl1};\n" \
                                      f"\t{valores[i].falseLabel}:\n" \
                                      f"\t{tmp1} = {tmp} + {i + 1}; // Dir. param{i + 1}\n" \
                                      f"\tSTACK[(int){tmp1}] = 0; // Asignar valor\n" \
                                      f"\t{lbl1}:\n\n"
                    # ! Generar código final
                    codigo += f"\tS = S + {entorno.size}; // Cambio de ámbito\n" \
                              f"\t{self.id}(); // Llamar función\n" \
                              f"\tS = S - {entorno.size}; // Cambio de ámbito\n"
                    # ! Retornar código

                    if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
                        # ! Obtener etiqueta de salida
                        lbl1 = generador.nuevoLabel()
                        # ! Reemplazar etiquetas
                        codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
                        # ! Agregar etiqueta al final
                        codigo += f"\t{lbl1}:\n"

                    return codigo
                else:
                    print("Error en los argumentos.")

            else:
                print("La cantidad de parametros '{}' no coincide con la cantidad de argumentos '{}'.".format(len(funcion.parametros), len(self.argumentos)))

        else:
            print("Funcion '{}' no encontrada.".format(self.id))
