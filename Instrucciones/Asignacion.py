from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Asignacion(Instruccion):
    def __init__(self, fila, id, expresion, indices=None):
        super().__init__(fila)
        self.id = id
        self.expresion = expresion
        self.indices = indices

    def convertir(self, generador, entorno):
        # ! Validar si existe la variable en la tabla de símbolos
        if entorno.existe_variable(self.id):
            # ! Obtener la variable y la depth
            variable, depth = entorno.obtener_variable(self.id)
            # ! Validar si la variable es mutable o no
            if variable.mutable:
                # ! Traducir la expresión y obtener el valor resultante
                valor = self.expresion.convertir(generador, entorno)
                # ! Validar que no haya ocurrido un error en la expresión al calcular el valor (None)
                if valor:
                    # ! Verificar el tipo de asignación (array | primitiva)
                    if self.indices is None:
                        # ! Retornar código generado en la asignación
                        return self.asignar_valor(generador, variable, depth, valor)
                    else:
                        # ! Validar si la variable es de tipo array
                        if variable.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                            # ! Recorrer los indices, traducirlos y obtener sus valores
                            valores = []
                            for indice in self.indices:
                                valores.append(indice.convertir(generador, entorno))
                            # ! Validar que ningún valor sea None
                            if None not in valores:
                                # ! Verificar que los valores sean I64
                                flag_correcto = True
                                for i in range(len(valores)):
                                    # ! Verificar el tipo
                                    if valores[i].tipo[0] != TipoPrimitivo.I64:
                                        # ! Actualizar la bandera
                                        flag_correcto = False
                                        break
                                if flag_correcto:
                                    # ! Verificar la depth
                                    if depth == 0:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t// ASIGNACION \n" \
                                                 f"\t{tmp1} = S + {variable.posicion}; \n" \
                                                 f"\t{tmp2} = STACK[(int){tmp1}]; \n"
                                        # ! Temporal auxiliarmp
                                        tmpn = tmp2
                                    else:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        # Crear código a retornar
                                        codigo = f"\t// ASIGNACION \n" \
                                                 f"\t{tmp1} = S - {depth}; \n" \
                                                 f"\t{tmp2} = {tmp1} + {variable.posicion}; \n" \
                                                 f"\t{tmp3} = STACK[(int){tmp2}]; \n"
                                        # ! Temporal auxilimpar
                                        tmpn = tmp3
                                    # ! Verificar si es referencia
                                    if variable.flag_reference:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        # ! Generar código
                                        codigo += f"\t{tmp1} = STACK[(int){tmpn}]; \n"
                                        # ! Temporal auxiliar
                                        tmpn = tmp1
                                    # ! Recorrer los valores obtenidos de los indices
                                    for i in range(len(valores)):
                                        # ! Verificar el tipo en esta dimension
                                        if variable.tipo[i] == TipoPrimitivo.ARREGLO:
                                            v = 1
                                        else:
                                            v = 2
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        # ! Generar códigomp
                                        codigo += f"\n\t \n" + valores[i].codigo + \
                                                  f"\t{tmp1} = {tmpn} + {v}; \n" \
                                                  f"\t{tmp2} = {tmp1} + {valores[i].reference}; \n\n"
                                        # ! Verificar si es el ultimo acceso
                                        if i == (len(valores) - 1):
                                            # ! Generar código
                                            codigo += "\n"
                                            # ! Temporal auxiliar
                                            tmpn = tmp2
                                        else:
                                            # ! Temporales auxiliares
                                            tmp1 = generador.nuevoTemp()
                                            # ! Generar código
                                            codigo += f"\n\t{tmp1} = HEAP[(int){tmp2}]; \n"
                                            # ! Temporal auxiliar
                                            tmpn = tmp1
                                    # ! Asignar el valor en el array y retornar el código generado
                                    return self.asignar_valor_array(generador, codigo, tmpn, valor)
                                else:
                                    alert = "Indices inflag_correcto."
                                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

                            else:
                                alert = "Error en los indices."
                                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                        else:
                            alert = "No se puede indexar un valor de tipo '{}'.".format(variable.tipo[0].value)
                            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                else:
                    alert = "Error en la expresion."
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            else:
                alert = "No se puede cambiar el valor de una variable inmutable."
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Variable '{}' no encontrada.".format(self.id)
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def asignar_valor(self, generador, variable, depth, valor):
        # ! Validar si no es booleano
        if valor.tipo != TipoPrimitivo.BOOL:
            # ! Verificar depth
            if depth == 0:
                # ! Verificar si es referencia
                if variable.flag_reference:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t// ASIGNACION \n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion}; \n" \
                                                                      f"\t{tmp2} = STACK[(int){tmp1}]; \n" \
                                                                      f"\tSTACK[(int){tmp2}] = {valor.reference}; \n"
                else:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t// ASIGNACION \n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion}; \n" \
                                                                      f"\tSTACK[(int){tmp1}] = {valor.reference}; \n"
            else:
                # ! Verificar si es referencia
                if variable.flag_reference:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t// ASIGNACION \n" + valor.codigo + f"\t{tmp1} = S - {depth}; \n" \
                                                                      f"\t{tmp2} = {tmp1} + {variable.posicion}; \n" \
                                                                      f"\t{tmp3} = STACK[(int){tmp2}]; \n" \
                                                                      f"\tSTACK[(int){tmp3}] = {valor.reference}; \n"
                else:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # Generar código
                    codigo = f"\t// ASIGNACION \n" + valor.codigo + f"\t{tmp1} = S - {depth}; \n" \
                                                                      f"\t{tmp2} = {tmp1} + {variable.posicion}; \n" \
                                                                      f"\tSTACK[(int){tmp2}] = {valor.reference}; \n"
        else:
            # ! Verificar depth
            if depth == 0:
                # ! Temporales auxiliares
                tmp1 = generador.nuevoTemp()
                # ! Labels auxiliares
                lbl1 = generador.nuevoLabel()
                # ! Generar código
                codigo = f"\t// ASIGNACION \n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                  f"\t{tmp1} = S + {variable.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp1}] = 1; \n" \
                                                                  f"\tgoto {lbl1};\n" \
                                                                  f"\t{valor.falseLabel}:\n" \
                                                                  f"\t{tmp1} = S + {variable.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp1}] = 0; \n" \
                                                                  f"\t{lbl1}:\n"
            else:
                # ! Temporales auxiliares
                tmp1 = generador.nuevoTemp()
                tmp2 = generador.nuevoTemp()
                # ! Labels auxiliares
                lbl1 = generador.nuevoLabel()
                # ! Generar código
                codigo = f"\t// ASIGNACION \n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                  f"\t{tmp1} = S - {depth}; \n" \
                                                                  f"\t{tmp2} = S + {variable.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp2}] = 1; \n" \
                                                                  f"\tgoto {lbl1};\n" \
                                                                  f"\t{valor.falseLabel}:\n" \
                                                                  f"\t{tmp1} = S - {depth}; \n" \
                                                                  f"\t{tmp2} = S + {variable.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp2}] = 0; \n" \
                                                                  f"\t{lbl1}:\n"
        if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
            # ! Obtener etiqueta de salida
            lbl1 = generador.nuevoLabel()
            # ! Reemplazar etiquetas
            codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
            # ! Agregar etiqueta al final
            codigo += f"\t{lbl1}:\n"
        # ! Retornar código
        return codigo

    def asignar_valor_array(self, generador, codigo, direccion, valor):
        # ! Validar si no es booleano
        if valor.tipo[0] != TipoPrimitivo.BOOL:
            # ! Generar código
            codigo += valor.codigo + f"\tHEAP[(int){direccion}] = {valor.reference}; \n"
        else:
            # ! Labels auxiliares
            lbl1 = generador.nuevoTemp()
            # ! Generar código
            codigo += valor.codigo + f"\t{valor.trueLabel}:\n" \
                                     f"\tHEAP[(int){direccion}] = 1; \n" \
                                     f"\tgoto {lbl1};\n" \
                                     f"\t{valor.falseLabel}:\n" \
                                     f"\tHEAP[(int){direccion}] = 0; \n" \
                                     f"\t{lbl1}:\n"
        # ! Retornar código
        if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
            # ! Obtener etiqueta de salida
            lbl1 = generador.nuevoLabel()
            # ! Reemplazar etiquetas
            codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
            # ! Agregar etiqueta al final
            codigo += f"\t{lbl1}:\n"
        return codigo
