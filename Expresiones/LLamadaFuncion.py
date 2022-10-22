from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class LlamadaFuncion(Expresion):
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
                    # ! Crear el dato a retornar
                    valor = Valor(self.fila, funcion.tipo)
                    # ! Temporal de entorno pivote
                    tmp = generador.nuevoTemp()
                    # ! Crear código a retornar
                    valor.codigo = f"\t// Llamada a función\n" \
                                   f"\t{tmp} = S + {entorno.size}; // Entorno simulado\n\n"
                    # ! Recorrer los datos de los argumentos
                    for i in range(len(valores)):
                        # ! Verificar el tipo
                        if valores[i].tipo[0] != TipoPrimitivo.BOOL:
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            # ! Generar código
                            valor.codigo += f"\t// Argumento\n" + valores[i].codigo + \
                                            f"\t{tmp1} = {tmp} + {i + 1}; // Dir. param{i + 1}\n" \
                                            f"\tSTACK[(int){tmp1}] = {valores[i].reference}; // Asignar valor\n\n"
                        else:
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            # ! Etiquetas auxiliares
                            lbl1 = generador.nuevoLabel()
                            # ! Generar código
                            valor.codigo += f"\t// Argumento\n" + valores[i].codigo + \
                                            f"\t{valores[i].trueLabel}:\n" \
                                            f"\t{tmp1} = {tmp} + {i + 1}; // Dir. param{i + 1}\n" \
                                            f"\tSTACK[(int){tmp1}] = 1; // Asignar valor\n" \
                                            f"\tgoto {lbl1};\n" \
                                            f"\t{valores[i].falseLabel}:\n" \
                                            f"\t{tmp1} = {tmp} + {i + 1}; // Dir. param{i + 1}\n" \
                                            f"\tSTACK[(int){tmp1}] = 0; // Asignar valor\n" \
                                            f"\t{lbl1}:\n\n"
                    # ! Verificar el tipo del dato
                    if valor.tipo[0] != TipoPrimitivo.BOOL:
                        # ! Temporales auxiliares
                        tmp1 = generador.nuevoTemp()
                        # ! Generar temporal de referencia
                        valor.reference = generador.nuevoTemp()
                        # ! Generar código final
                        valor.codigo += f"\tS = S + {entorno.size}; // Cambio de ámbito\n" \
                                        f"\t{self.id}(); // Llamar función\n" \
                                        f"\t{tmp1} = S + 0; // Dir. return\n" \
                                        f"\t{valor.reference} = STACK[(int){tmp1}]; // Valor return\n" \
                                        f"\tS = S - {entorno.size}; // Cambio de ámbito\n\n"
                    else:
                        # ! Temporales auxiliares
                        tmp1 = generador.nuevoTemp()
                        tmp2 = generador.nuevoTemp()
                        # ! Generar etiquetas booleanas
                        valor.trueLabel = generador.nuevoLabel()
                        valor.falseLabel = generador.nuevoLabel()
                        # ! Generar código final
                        valor.codigo += f"\tS = S + {entorno.size}; // Cambio de ámbito\n" \
                                        f"\t{self.id}(); // Llamar función\n" \
                                        f"\t{tmp1} = S + 0; // Dir. return\n" \
                                        f"\t{tmp2} = STACK[(int){tmp1}]; // Valor return\n" \
                                        f"\tS = S - {entorno.size}; // Cambio de ámbito\n\n" \
                                        f"\tif ({tmp2}) goto {valor.trueLabel};\n" \
                                        f"\tgoto {valor.falseLabel};\n"
                    # ! Retornar dato
                    return valor
                else:
                    print("Error en los argumentos.")

            else:
                print("La cantidad de parametros '{}' no coincide con la cantidad de argumentos '{}'.".format(len(funcion.parametros), len(self.argumentos)))

        else:
            print("Funcion '{}' no encontrada.".format(self.id))
