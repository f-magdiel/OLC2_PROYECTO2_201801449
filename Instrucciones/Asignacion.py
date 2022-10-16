from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo


class Asignacion(Instruccion):
    def __init__(self, fila, id, expresion, indices=None):
        super().__init__(fila)
        self.id = id
        self.expresion = expresion
        self.indices = indices


    def convertir(self, generador, entorno):
        # Validar si existe la variable en la tabla de símbolos
        if entorno.existe_variable(self.id):
            # Obtener la variable y la profundidad
            variable, profundidad = entorno.obtener_variable(self.id)
            # Validar si la variable es mutable o no
            if variable.mutable:
                # Traducir la expresión y obtener el dato resultante
                dato = self.expresion.convertir(generador, entorno)
                # Validar que no haya ocurrido un error en la expresión al calcular el dato (None)
                if dato:
                    # Verificar el tipo de asignación (array | primitiva)
                    if self.indices is None:
                        # Retornar código generado en la asignación
                        return self.asignar_valor(generador, variable, profundidad, dato)
                    else:
                        # Validar si la variable es de tipo array
                        if variable.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                            # Recorrer los indices, traducirlos y obtener sus datos
                            datos = []
                            for indice in self.indices:
                                datos.append(indice.convertir(generador, entorno))
                            # Validar que ningún dato sea None
                            if None not in datos:
                                # Verificar que los datos sean I64
                                correctos = True
                                for i in range(len(datos)):
                                    # Verificar el tipo
                                    if datos[i].tipo[0] != TipoPrimitivo.I64:
                                        # Actualizar la bandera
                                        correctos = False
                                        break
                                if correctos:
                                    # Verificar la profundidad
                                    if profundidad == 0:
                                        # Temporales auxiliares
                                        t1 = generador.nuevoTemp()
                                        t2 = generador.nuevoTemp()
                                        # Crear código a retornar
                                        codigo = f"\t/* ASIGNACIÓN */\n" \
                                                 f"\t{t1} = S + {variable.posicion}; // Dir. variable\n" \
                                                 f"\t{t2} = STACK[(int){t1}]; // Acceso 1\n"
                                        # Temporal auxiliar
                                        tn = t2
                                    else:
                                        # Temporales auxiliares
                                        t1 = generador.nuevoTemp()
                                        t2 = generador.nuevoTemp()
                                        t3 = generador.nuevoTemp()
                                        # Crear código a retornar
                                        codigo = f"\t/* ASIGNACIÓN */\n" \
                                                 f"\t{t1} = S - {profundidad}; // Entorno pivote\n" \
                                                 f"\t{t2} = {t1} + {variable.posicion}; // Dir. variable\n" \
                                                 f"\t{t3} = STACK[(int){t2}]; // Acceso 1\n"
                                        # Temporal auxiliar
                                        tn = t3
                                    # Verificar si es referencia
                                    if variable.flag_reference:
                                        # Temporales auxiliares
                                        t1 = generador.nuevoTemp()
                                        # Generar código
                                        codigo += f"\t{t1} = STACK[(int){tn}]; // Acceso 2\n"
                                        # Temporal auxiliar
                                        tn = t1
                                    # Recorrer los datos obtenidos de los indices
                                    for i in range(len(datos)):
                                        # Verificar el tipo en esta dimension
                                        if variable.tipo[i] == TipoPrimitivo.ARREGLO:
                                            v = 1
                                        else:
                                            v = 2
                                        # Temporales auxiliares
                                        t1 = generador.nuevoTemp()
                                        t2 = generador.nuevoTemp()
                                        # Generar código
                                        codigo += f"\n\t// Indice\n" + datos[i].codigo + \
                                                  f"\t{t1} = {tn} + {v}; // Pivote valores\n" \
                                                  f"\t{t2} = {t1} + {datos[i].reference}; // Indice en C3D\n\n"
                                        # Verificar si es el ultimo acceso
                                        if i == (len(datos) - 1):
                                            # Generar código
                                            codigo += "\n"
                                            # Temporal auxiliar
                                            tn = t2
                                        else:
                                            # Temporales auxiliares
                                            t1 = generador.nuevoTemp()
                                            # Generar código
                                            codigo += f"\n\t{t1} = HEAP[(int){t2}]; // Nuevo acceso\n"
                                            # Temporal auxiliar
                                            tn = t1
                                    # Asignar el valor en el array y retornar el código generado
                                    return self.asignar_valor_array(generador, codigo, tn, dato)
                                else:
                                    print("Indices incorrectos.")

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

    def asignar_valor(self, generador, variable, profundidad, dato):
        # Validar si no es booleano
        if dato.tipo != TipoPrimitivo.BOOL:
            # Verificar profundidad
            if profundidad == 0:
                # Verificar si es referencia
                if variable.flag_reference:
                    # Temporales auxiliares
                    t1 = generador.nuevoTemp()
                    t2 = generador.nuevoTemp()
                    # Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + dato.codigo + f"\t{t1} = S + {variable.posicion}; // Ref.\n" \
                                                                     f"\t{t2} = STACK[(int){t1}]; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){t2}] = {dato.reference}; // Asignar\n"
                else:
                    # Temporales auxiliares
                    t1 = generador.nuevoTemp()
                    # Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + dato.codigo + f"\t{t1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){t1}] = {dato.reference}; // Asignar\n"
            else:
                # Verificar si es referencia
                if variable.flag_reference:
                    # Temporales auxiliares
                    t1 = generador.nuevoTemp()
                    t2 = generador.nuevoTemp()
                    t3 = generador.nuevoTemp()
                    # Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + dato.codigo + f"\t{t1} = S - {profundidad}; // Entorno pivote\n" \
                                                                     f"\t{t2} = {t1} + {variable.posicion}; // Ref.\n" \
                                                                     f"\t{t3} = STACK[(int){t2}]; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){t3}] = {dato.reference}; // Asignar\n"
                else:
                    # Temporales auxiliares
                    t1 = generador.nuevoTemp()
                    t2 = generador.nuevoTemp()
                    # Generar código
                    codigo = f"\t/* ASIGNACIÓN */\n" + dato.codigo + f"\t{t1} = S - {profundidad}; // Entorno pivote\n" \
                                                                     f"\t{t2} = {t1} + {variable.posicion}; // Dir. variable\n" \
                                                                     f"\tSTACK[(int){t2}] = {dato.reference}; // Asignar\n"
        else:
            # Verificar profundidad
            if profundidad == 0:
                # Temporales auxiliares
                t1 = generador.nuevoTemp()
                # Labels auxiliares
                l1 = generador.nuevoLabel()
                # Generar código
                codigo = f"\t/* ASIGNACIÓN */\n" + dato.codigo + f"\t{dato.trueLabel}:\n" \
                                                                 f"\t{t1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){t1}] = 1; // Asignar\n" \
                                                                 f"\tgoto {l1};\n" \
                                                                 f"\t{dato.falseLabel}:\n" \
                                                                 f"\t{t1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){t1}] = 0; // Asignar\n" \
                                                                 f"\t{l1}:\n"
            else:
                # Temporales auxiliares
                t1 = generador.nuevoTemp()
                t2 = generador.nuevoTemp()
                # Labels auxiliares
                l1 = generador.nuevoLabel()
                # Generar código
                codigo = f"\t/* ASIGNACIÓN */\n" + dato.codigo + f"\t{dato.trueLabel}:\n" \
                                                                 f"\t{t1} = SP - {profundidad}; // Entorno pivote\n" \
                                                                 f"\t{t2} = SP + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){t2}] = 1; // Asignar\n" \
                                                                 f"\tgoto {l1};\n" \
                                                                 f"\t{dato.falseLabel}:\n" \
                                                                 f"\t{t1} = S - {profundidad}; // Entorno pivote\n" \
                                                                 f"\t{t2} = S + {variable.posicion}; // Dir. variable\n" \
                                                                 f"\tSTACK[(int){t2}] = 0; // Asignar\n" \
                                                                 f"\t{l1}:\n"
        # Retornar código
        return codigo

    def asignar_valor_array(self, generador, codigo, direccion, dato):
        # Validar si no es booleano
        if dato.tipo != TipoPrimitivo.BOOL:
            # Generar código
            codigo += dato.codigo + f"\tHEAP[(int){direccion}] = {dato.reference}; // Asignar\n"
        else:
            # Labels auxiliares
            l1 = generador.nuevoTemp()
            # Generar código
            codigo += dato.codigo + f"\t{dato.trueLabel}:\n" \
                                    f"\tHEAP[(int){direccion}] = 1; // Asignar\n" \
                                    f"\tgoto {l1};\n" \
                                    f"\t{dato.falseLabel}:\n" \
                                    f"\tHEAP[(int){direccion}] = 0; // Asignar\n" \
                                    f"\t{l1}:\n"
        # Retornar código
        return codigo



    #     if entorno.existe_variable(self.id):
    #         var, depth = entorno.obtener_variable(self.id)
    #         if var.mutable:
    #             valor = self.expresion.convertir(generador, entorno)
    #             if valor:
    #                 if self.indices is None:
    #                     return self.asignacion_val(generador, var, depth, valor)
    #                 else:
    #                     if var.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
    #                         valores = []
    #                         for indice in self.indices:
    #                             valores.append(indice.convertir(generador, entorno))
    #
    #                         # ! Validar que un valor no sea vacio
    #                         if None not in valores:
    #                             flag_correcto = True
    #                             for i in range(len(valores)):
    #                                 if valores[i].tipo[0] != TipoPrimitivo.I64:
    #                                     flag_correcto = False
    #                                     break
    #                             if flag_correcto:
    #                                 if depth == 0:
    #                                     # ! Temporales aux
    #                                     tmp1 = generador.nuevoTemp()
    #                                     tmp2 = generador.nuevoTemp()
    #
    #                                     codigo = f"\t/* ASIGNACIÓN */\n" \
    #                                              f"\t{tmp1} = S + {var.posicion}; // Dir. var\n" \
    #                                              f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. array\n\n"
    #                                     tmp = tmp2
    #                                 else:
    #                                     # ! Temporales aux
    #                                     tmp1 = generador.nuevoTemp()
    #                                     tmp2 = generador.nuevoTemp()
    #                                     tmp3 = generador.nuevoTemp()
    #
    #                                     codigo = f"\t/* ASIGNACIÓN */\n" \
    #                                              f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
    #                                              f"\t{tmp2} = {tmp1} + {var.posicion}; // Dir. var\n" \
    #                                              f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. array\n\n"
    #                                     tmp = tmp3
    #
    #                                 for i in range(len(valores)):
    #                                     if var.tipo[0] == TipoPrimitivo.ARREGLO:
    #                                         val = 1
    #                                     else:
    #                                         val = 2
    #                                     tmp1 = generador.nuevoTemp()
    #                                     tmp2 = generador.nuevoTemp()
    #
    #                                     codigo += f"\t// Indice\n" + valores[i].codigo + \
    #                                               f"\t{tmp1} = {tmp} + {val}; // Pivote valores\n" \
    #                                               f"\t{tmp2} = {tmp1} + {valores[i].reference}; // Indice en C3D\n\n"
    #
    #                                 return self.asignacion_arr(generador, codigo, tmp, valor)
    #                             else:
    #                                 print("Error")
    #                         else:
    #                             print("Error")
    #                     else:
    #                         print("Error")
    #             else:
    #                 print("Error")
    #         else:
    #             print("Error")
    #     else:
    #         print("Error en encontrar variable")
    #
    # def asignacion_val(self, generador, variable, depth, valor):
    #     if valor.tipo != TipoPrimitivo.BOOL:
    #         if depth == 0:
    #             tmp1 = generador.nuevoTemp()
    #             codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. var\n" \
    #                                                               f"\tSTACK[(int){tmp1}] = {valor.reference}; // Asignar\n"
    #             # Retornar código
    #             return codigo
    #         else:
    #             # ! Temporales aux
    #             tmp1 = generador.nuevoTemp()
    #             tmp2 = generador.nuevoTemp()
    #             # ! Se genera código
    #             codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
    #                                                               f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. var\n" \
    #                                                               f"\tSTACK[(int){tmp2}] = {valor.reference}; // Asignar\n"
    #             return codigo
    #     else:
    #         # ! Validar profundidad
    #         if depth:
    #             # ! Temporal y Label aux
    #             tmp1 = generador.nuevoTemp()
    #             lbl1 = generador.nuevoLabel()
    #
    #             codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
    #                                                               f"\t{tmp1} = S + {variable.posicion}; // Dir. var\n" \
    #                                                               f"\tSTACK[(int){tmp1}] = 1; // Asignar\n" \
    #                                                               f"\tgoto {lbl1};\nbl" \
    #                                                               f"\t{valor.falseLabel}:\n" \
    #                                                               f"\t{tmp1} = S + {variable.posicion}; // Dir. var\n" \
    #                                                               f"\tSTACK[(int){tmp1}] = 0; // Asignar\n" \
    #                                                               f"\t{lbl1}:\n"
    #             return codigo
    #         else:
    #             # ! Temporales  y Label aux
    #             tmp1 = generador.nuevoTemp()
    #             tmp2 = generador.nuevoTemp()
    #             lbl1 = generador.nuevoLabel()
    #
    #             codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
    #                                                               f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
    #                                                               f"\t{tmp2} = S + {variable.posicion}; // Dir. var\n" \
    #                                                               f"\tSTACK[(int){tmp2}] = 1; // Asignar\n" \
    #                                                               f"\tgoto {lbl1};\n" \
    #                                                               f"\t{valor.falseLabel}:\n" \
    #                                                               f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
    #                                                               f"\t{tmp2} = S + {variable.posicion}; // Dir. var\n" \
    #                                                               f"\tSTACK[(int){tmp2}] = 0; // Asignar\n" \
    #                                                               f"\t{lbl1}:\n"
    #
    #             return codigo
    #
    # def asignacion_arr(self, generador, codigo, dir, valor):
    #     if valor.tipo != TipoPrimitivo.BOOL:
    #         codigo += valor.codigo + f"\tHEAP[(int){dir}] = {valor.reference}; // Asignar\n"
    #         return codigo
    #     else:
    #         lbl1 = generador.nuevoLabel()
    #         codigo += valor.codigo + f"\t{valor.trueLabel}:\n" \
    #                                  f"\tHEAP[(int){dir}] = 1; // Asignar\n" \
    #                                  f"\tgoto {lbl1};\n" \
    #                                  f"\t{valor.falseLabel}:\n" \
    #                                  f"\tHEAP[(int){dir}] = 0; // Asignar\n" \
    #                                  f"\t{lbl1}:\n"
    #         return codigo
