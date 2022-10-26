from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


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
                    codigo = f"\t// LLAMAR FUN \n" \
                             f"\t{tmp} = S + {entorno.size}; \n\n"
                    # ! Recorrer los datos de los argumentos
                    for i in range(len(valores)):
                        # ! Verificar el tipo
                        if valores[i].tipo[0] != TipoPrimitivo.BOOL:
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            # ! Generar código
                            codigo += f"\t \n" + valores[i].codigo + \
                                      f"\t{tmp1} = {tmp} + {i + 1}; \n" \
                                      f"\tSTACK[(int){tmp1}] = {valores[i].reference}; \n\n"
                        else:
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            # ! Etiquetas auxiliares
                            lbl1 = generador.nuevoLabel()
                            # ! Generar código
                            codigo += f"\t \n" + valores[i].codigo + \
                                      f"\t{valores[i].trueLabel}:\n" \
                                      f"\t{tmp1} = {tmp} + {i + 1}; \n" \
                                      f"\tSTACK[(int){tmp1}] = 1; \n" \
                                      f"\tgoto {lbl1};\n" \
                                      f"\t{valores[i].falseLabel}:\n" \
                                      f"\t{tmp1} = {tmp} + {i + 1}; \n" \
                                      f"\tSTACK[(int){tmp1}] = 0; \n" \
                                      f"\t{lbl1}:\n\n"
                    # ! Generar código final
                    codigo += f"\tS = S + {entorno.size}; \n" \
                              f"\t{self.id}(); \n" \
                              f"\tS = S - {entorno.size}; \n"
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
                    alert = "Error en los argumentos."
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

            else:
                alert = "La cantidad de parametros '{}' no coincide con la cantidad de argumentos '{}'.".format(len(funcion.parametros), len(self.argumentos))
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Funcion '{}' no encontrada.".format(self.id)
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
