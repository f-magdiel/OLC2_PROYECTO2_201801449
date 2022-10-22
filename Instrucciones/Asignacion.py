from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo


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
                                        codigo = f"\t/* ASIGNACIÓN */\n" \
                                                 f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                 f"\t{tmp2} = STACK[(int){tmp1}]; // Acceso 1\n"
                                        # ! Temporal auxiliarmp
                                        tmpn = tmp2
                                    else:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        # Crear código a retornar
                                        codigo = f"\t/* ASIGNACIÓN */\n" \
                                                 f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                 f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                                 f"\t{tmp3} = STACK[(int){tmp2}]; // Acceso 1\n"
                                        # ! Temporal auxilimpar
                                        tmpn = tmp3
                                    # ! Verificar si es referencia
                                    if variable.flag_reference:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        # ! Generar código
                                        codigo += f"\t{tmp1} = STACK[(int){tmpn}]; // Acceso 2\n"
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
                                        codigo += f"\n\t// Indice\n" + valores[i].codigo + \
                                                  f"\t{tmp1} = {tmpn} + {v}; // Pivote valores\n" \
                                                  f"\t{tmp2} = {tmp1} + {valores[i].reference}; // Indice en C3D\n\n"
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
                                            codigo += f"\n\t{tmp1} = HEAP[(int){tmp2}]; // Nuevo acceso\n"
                                            # ! Temporal auxiliar
                                            tmpn = tmp1
                                    # ! Asignar el valor en el array y retornar el código generado
                                    return self.asignar_valor_array(generador, codigo, tmpn, valor)
                                else:
                                    print("Indices inflag_correcto.")

                            else:
                                print("Error en los indices.")

                        else:
                            print("No se puede indexar un valor de tipo '{}'.".format(variable.tipo[0].value))

                else:
                    print("Error en la expresion.")

            else:
                print("No se puede cambiar el valor de una variable inmutable.")

        else:
            print("Variable '{}' no encontrada.".format(self.id))


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
                    codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion}; // Ref.\n" \
                                                                     f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){tmp2}] = {valor.reference}; // Asignar\n"
                else:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){tmp1}] = {valor.reference}; // Asignar\n"
            else:
                # ! Verificar si es referencia
                if variable.flag_reference:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                     f"\t{tmp2} = {tmp1} + {variable.posicion}; // Ref.\n" \
                                                                     f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){tmp3}] = {valor.reference}; // Asignar\n"
                else:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                     f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){tmp2}] = {valor.reference}; // Asignar\n"
        else:
            # ! Verificar depth
            if depth == 0:
                # ! Temporales auxiliares
                tmp1 = generador.nuevoTemp()
                # ! Labels auxiliares
                lbl1 = generador.nuevoLabel()
                # ! Generar código
                codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                 f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){tmp1}] = 1; // Asignar\n" \
                                                                 f"\tgoto {lbl1};\n" \
                                                                 f"\t{valor.falseLabel}:\n" \
                                                                 f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){tmp1}] = 0; // Asignar\n" \
                                                                 f"\t{lbl1}:\n"
            else:
                # ! Temporales auxiliares
                tmp1 = generador.nuevoTemp()
                tmp2 = generador.nuevoTemp()
                # ! Labels auxiliares
                lbl1 = generador.nuevoLabel()
                # ! Generar código
                codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                 f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                 f"\t{tmp2} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){tmp2}] = 1; // Asignar\n" \
                                                                 f"\tgoto {lbl1};\n" \
                                                                 f"\t{valor.falseLabel}:\n" \
                                                                 f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                 f"\t{tmp2} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){tmp2}] = 0; // Asignar\n" \
                                                                 f"\t{lbl1}:\n"
        # ! Retornar código
        return codigo

    def asignar_valor_array(self, generador, codigo, direccion, valor):
        # ! Validar si no es booleano
        if valor.tipo[0] != TipoPrimitivo.BOOL:
            # ! Generar código
            codigo += valor.codigo + f"\tHEAP[(int){direccion}] = {valor.reference}; // Asignar\n"
        else:
            # ! Labels auxiliares
            lbl1 = generador.nuevoTemp()
            # ! Generar código
            codigo += valor.codigo + f"\t{valor.trueLabel}:\n" \
                                    f"\tHEAP[(int){direccion}] = 1; // Asignar\n" \
                                    f"\tgoto {lbl1};\n" \
                                    f"\t{valor.falseLabel}:\n" \
                                    f"\tHEAP[(int){direccion}] = 0; // Asignar\n" \
                                    f"\t{lbl1}:\n"
        # ! Retornar código
        return codigo

