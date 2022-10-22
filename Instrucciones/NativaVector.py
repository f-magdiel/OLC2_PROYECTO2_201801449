from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Enum.Nativas import NATIVAS


class NativaVector(Instruccion):
    def __init__(self, fila, id, funcion, exp1, exp2):
        super().__init__(fila)
        self.funcion = funcion
        self.exp1 = exp1
        self.exp2 = exp2
        self.id = id

    def convertir(self, generador, entorno):
        # ! Validar si existe la variable en la tabla de símbolos
        if entorno.existe_variable(self.id):
            # ! Obtener la variable y la depth
            variable, depth = entorno.obtener_variable(self.id)
            # ! Validar si la variable es mutable o no
            if variable.mutable:
                # ! Validar si la variables es de tipo VECTOR
                if variable.tipo[0] == TipoPrimitivo.VECTOR:
                    # ! PUSH
                    if self.funcion == NATIVAS.PUSH:
                        # ! Traducir la expresión y obtener el dato resultante
                        valor_1 = self.exp1.convertir(generador, entorno)
                        # ! Validar que no haya ocurrido un error en la expresión al calcular el dato (None)
                        if valor_1:
                            # ! Parte de codigo inicial para el dato
                            if valor_1.tipo[0] != TipoPrimitivo.BOOL:
                                aux_codigo = valor_1.codigo
                            else:
                                aux_codigo = ""
                            # ! Verificar depth
                            if depth == 0:
                                # ! Verificar si es referencia
                                if variable.flag_reference:
                                    # ! Temporales auxiliares
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    tmp3 = generador.nuevoTemp()
                                    # ! Crear código a retornar
                                    codigo = f"\t/* PUSH() */\n" + aux_codigo + f"\t{tmp1} = S + {variable.posicion}; // Ref.\n" \
                                                                                f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. variable\n" \
                                                                                f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                    # ! Temporales de dirección
                                    tmpd = tmp2
                                    tmpv = tmp3
                                else:
                                    # ! Temporales auxiliares
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    # ! Crear código a retornar
                                    codigo = f"\t/* PUSH() */\n" + aux_codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                                f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. vector\n\n"
                                    # ! Temporales de dirección
                                    tmpd = tmp1
                                    tmpv = tmp2
                            else:
                                # ! Verificar si es referencia
                                if variable.flag_reference:
                                    # ! Temporales auxiliares
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    tmp3 = generador.nuevoTemp()
                                    tmp4 = generador.nuevoTemp()
                                    # ! Crear código a retornar
                                    codigo = f"\t/* PUSH() */\n" + aux_codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                f"\t{tmp2} = {tmp1} + {variable.posicion}; // Ref.\n" \
                                                                                f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. variable\n" \
                                                                                f"\t{tmp4} = STACK[(int){tmp3}]; // Dir. vector\n\n"
                                    # ! Temporales de dirección
                                    tmpd = tmp3
                                    tmpv = tmp4
                                else:
                                    # ! Temporales auxiliares
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    tmp3 = generador.nuevoTemp()
                                    # ! Crear código a retornar
                                    codigo = f"\t/* PUSH() */\n" + aux_codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                                                                f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                    # ! Temporales de dirección
                                    tmpd = tmp2
                                    tmpv = tmp3
                            # ! Temporales auxiliares
                            tmp1 = generador.nuevoTemp()
                            tmp2 = generador.nuevoTemp()
                            tmp3 = generador.nuevoTemp()
                            tmp4 = generador.nuevoTemp()
                            tmp5 = generador.nuevoTemp()
                            tmp6 = generador.nuevoTemp()
                            tmp7 = generador.nuevoTemp()
                            tmp8 = generador.nuevoTemp()
                            tmp9 = generador.nuevoTemp()
                            tmp10 = generador.nuevoTemp()
                            tmp11 = generador.nuevoTemp()
                            # ! Etiquetas auxiliares
                            lbl1 = generador.nuevoLabel()
                            lbl2 = generador.nuevoLabel()
                            lbl3 = generador.nuevoLabel()
                            lbl4 = generador.nuevoLabel()
                            lbl5 = generador.nuevoLabel()
                            lbl6 = generador.nuevoLabel()
                            # ! Generar código
                            codigo += f"\t{tmp1} = H; // Nueva referencia\n\n" \
                                      f"\t// Migrar len\n" \
                                      f"\t{tmp2} = {tmpv} + 0; // Dir. len anterior\n" \
                                      f"\t{tmp3} = HEAP[(int){tmp2}]; // len anterior\n" \
                                      f"\t{tmp4} = {tmp3} + 1; // len anterior + 1\n" \
                                      f"\tHEAP[(int)H] = {tmp4};\n" \
                                      f"\tH = H + 1;\n\n" \
                                      f"\t// Migrar capacity\n" \
                                      f"\t{tmp5} = {tmpv} + 1; // Dir. capacity anterior\n" \
                                      f"\t{tmp6} = HEAP[(int){tmp5}]; // capacity anterior\n" \
                                      f"\tif ({tmp6} <= {tmp4}) goto {lbl1}; // capacity anterior <= len\n" \
                                      f"\tgoto {lbl2};\n" \
                                      f"\t{lbl1}:\n" \
                                      f"\t{tmp7} = {tmp6} * 2; // capacity anterior * 2\n" \
                                      f"\tHEAP[(int)H] = {tmp7};\n" \
                                      f"\tH = H + 1;\n" \
                                      f"\tgoto {lbl3};\n" \
                                      f"\t{lbl2}:\n" \
                                      f"\tHEAP[(int)H] = {tmp6};\n" \
                                      f"\tH = H + 1;\n" \
                                      f"\t{lbl3}:\n\n" \
                                      f"\t// Migrar valores\n" \
                                      f"\t{tmp8} = 0; // i\n" \
                                      f"\t{lbl6}:\n" \
                                      f"\tif ({tmp8} < {tmp3}) goto {lbl4}; // i < len anterior\n" \
                                      f"\tgoto {lbl5};\n" \
                                      f"\t{lbl4}:\n" \
                                      f"\t{tmp9} = {tmpv} + 2; // Pivote de valores\n" \
                                      f"\t{tmp10} = {tmp9} + {tmp8}; // Dir. valor\n" \
                                      f"\t{tmp11} = HEAP[(int){tmp10}]; // valor\n" \
                                      f"\tHEAP[(int)H] = {tmp11};\n" \
                                      f"\tH = H + 1;\n\n" \
                                      f"\t{tmp8} = {tmp8} + 1; // i++\n" \
                                      f"\tgoto {lbl6};\n" \
                                      f"\t{lbl5}:\n\n"
                            # ! Verificar el tipo del dato
                            if valor_1.tipo[0] != TipoPrimitivo.BOOL:
                                # ! Generar código
                                codigo += f"\tHEAP[(int)H] = {valor_1.reference};\n" \
                                          f"\tH = H + 1;\n\n"
                            else:
                                # ! Labels auxiliares
                                lbl1 = generador.nuevoLabel()
                                # ! Generar código
                                codigo += valor_1.codigo + f"\t{valor_1.trueLabel}:\n" \
                                                           f"\tHEAP[(int)H] = 1;\n" \
                                                           f"\tH = H + 1;\n" \
                                                           f"\tgoto {lbl1};\n" \
                                                           f"\t{valor_1.falseLabel}:\n" \
                                                           f"\tHEAP[(int)H] = 0;\n" \
                                                           f"\tH = H + 1;\n" \
                                                           f"\t{lbl1}:\n\n"
                            # ! Generar código para cambio de referencia
                            codigo += f"\tSTACK[(int){tmpd}] = {tmp1}; // Cambio de referencia\n"
                            # ! Retornar código
                            return codigo
                        else:
                            print("Error en la expresion.")

                    # ! INSERT
                    elif self.funcion == NATIVAS.INSERT:
                        # ! Traducir las expresiones y obtener los datos resultantes
                        valor_1 = self.exp1.convertir(generador, entorno)
                        valor_2 = self.exp2.convertir(generador, entorno)
                        # ! Validar que no haya ocurrido un error en las expresiones al calcular el dato (None)
                        if valor_1 and valor_2:
                            # ! Validar que el valor_1 sea de tipo I64
                            if valor_1.tipo[0] == TipoPrimitivo.I64:
                                # ! Parte de codigo inicial para el dato
                                if valor_1.tipo[0] != TipoPrimitivo.BOOL:
                                    aux_codigo = valor_2.codigo
                                else:
                                    aux_codigo = ""
                                # ! Verificar depth
                                if depth == 0:
                                    # ! Verificar si es referencia
                                    if variable.flag_reference:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* INSERT() */\n" + valor_1.codigo + aux_codigo + f"\t{tmp1} = S + {variable.posicion}; // Ref.\n" \
                                                                                                       f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. variable\n\n" \
                                                                                                       f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp2
                                        tmpv = tmp3
                                    else:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* INSERT() */\n" + valor_1.codigo + aux_codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                                                       f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp1
                                        tmpv = tmp2
                                else:
                                    # ! Verificar si es referencia
                                    if variable.flag_reference:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        tmp4 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* INSERT() */\n" + valor_1.codigo + aux_codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                                       f"\t{tmp2} = {tmp1} + {variable.posicion}; // Ref.\n" \
                                                                                                       f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. variable\n" \
                                                                                                       f"\t{tmp4} = STACK[(int){tmp3}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp3
                                        tmpv = tmp4
                                    else:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* INSERT() */\n" + valor_1.codigo + aux_codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                                       f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                                                                                       f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp2
                                        tmpv = tmp3
                                # ! Temporales auxiliares
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                tmp3 = generador.nuevoTemp()
                                tmp4 = generador.nuevoTemp()
                                tmp5 = generador.nuevoTemp()
                                tmp6 = generador.nuevoTemp()
                                tmp7 = generador.nuevoTemp()
                                tmp8 = generador.nuevoTemp()
                                tmp9 = generador.nuevoTemp()
                                tmp10 = generador.nuevoTemp()
                                tmp11 = generador.nuevoTemp()
                                # ! Etiquetas auxiliares
                                lbl1 = generador.nuevoLabel()
                                lbl2 = generador.nuevoLabel()
                                lbl3 = generador.nuevoLabel()
                                lbl4 = generador.nuevoLabel()
                                lbl5 = generador.nuevoLabel()
                                lbl6 = generador.nuevoLabel()
                                lbl7 = generador.nuevoLabel()
                                lbl8 = generador.nuevoLabel()
                                lbl9 = generador.nuevoLabel()
                                lbl10 = generador.nuevoLabel()
                                # ! Generar código
                                codigo += f"\t{tmp1} = H; // Nueva referencia\n\n" \
                                          f"\t// Migrar len\n" \
                                          f"\t{tmp2} = {tmpv} + 0; // Dir. len anterior\n" \
                                          f"\t{tmp3} = HEAP[(int){tmp2}]; // len anterior\n" \
                                          f"\t{tmp4} = {tmp3} + 1; // len anterior + 1\n" \
                                          f"\tHEAP[(int)H] = {tmp4};\n" \
                                          f"\tH = H + 1;\n\n" \
                                          f"\t// Migrar capacity\n" \
                                          f"\t{tmp5} = {tmpv} + 1; // Dir. capacity anterior\n" \
                                          f"\t{tmp6} = HEAP[(int){tmp5}]; // capacity anterior\n" \
                                          f"\tif ({tmp6} <= {tmp4}) goto {lbl1}; // capacity anterior <= len\n" \
                                          f"\tgoto {lbl2};\n" \
                                          f"\t{lbl1}:\n" \
                                          f"\t{tmp7} = {tmp6} * 2; // capacity anterior * 2\n" \
                                          f"\tHEAP[(int)H] = {tmp7};\n" \
                                          f"\tH = H + 1;\n" \
                                          f"\tgoto {lbl3};\n" \
                                          f"\t{lbl2}:\n" \
                                          f"\tHEAP[(int)H] = {tmp6};\n" \
                                          f"\tH = H + 1;\n" \
                                          f"\t{lbl3}:\n\n" \
                                          f"\t// Migrar valores\n" \
                                          f"\t{tmp8} = 0; // i\n" \
                                          f"\t{lbl6}:\n" \
                                          f"\tif ({tmp8} < {tmp3}) goto {lbl4}; // i < len anterior\n" \
                                          f"\tgoto {lbl5};\n" \
                                          f"\t{lbl4}:\n" \
                                          f"\t{tmp9} = {tmpv} + 2; // Pivote de valores\n" \
                                          f"\t{tmp10} = {tmp9} + {tmp8}; // Dir. valor\n" \
                                          f"\t{tmp11} = HEAP[(int){tmp10}]; // valor\n\n" \
                                          f"\tif ({tmp8} == {valor_1.reference}) goto {lbl7}; // i == indice insert\n" \
                                          f"\tgoto {lbl8};\n" \
                                          f"\t{lbl7}:\n"
                                # ! Verificar el tipo del dato
                                if valor_1.tipo[0] != TipoPrimitivo.BOOL:
                                    # ! Generar código
                                    codigo += f"\tHEAP[(int)H] = {valor_2.reference};\n" \
                                              f"\tH = H + 1;\n"
                                else:
                                    # ! Labels auxiliares
                                    lbla = generador.obtener_label()
                                    # ! Generar código
                                    codigo += valor_2.codigo + f"\t{valor_2.trueLabel}:\n" \
                                                               f"\tHEAP[(int)H] = 1;\n" \
                                                               f"\tH = H + 1;\n" \
                                                               f"\tgoto {lbla};\n" \
                                                               f"\t{valor_2.falseLabel}:\n" \
                                                               f"\tHEAP[(int)H] = 0;\n" \
                                                               f"\tH = H + 1;\n" \
                                                               f"\t{lbla}:\n"
                                # ! Generar código
                                codigo += f"\t{lbl8}:\n\n" \
                                          f"\tHEAP[(int)H] = {tmp11};\n" \
                                          f"\tH = H + 1;\n\n" \
                                          f"\t{tmp8} = {tmp8} + 1; // i++\n" \
                                          f"\tgoto {lbl6};\n" \
                                          f"\t{lbl5}:\n\n" \
                                          f"\t// Verificar si era insert al final\n" \
                                          f"\tif ({valor_1.reference} == {tmp3}) goto {lbl9};\n" \
                                          f"\tgoto {lbl10};\n" \
                                          f"\t{lbl9}:\n"

                                if valor_1.tipo[0] != TipoPrimitivo.BOOL:
                                    # ! Generar código
                                    codigo += f"\tHEAP[(int)H] = {valor_2.reference};\n" \
                                              f"\tH = H + 1;\n"
                                else:
                                    # ! Labels auxiliares
                                    lbla = generador.nuevoLabel()
                                    # ! Generar código
                                    codigo += valor_2.codigo + f"\t{valor_2.trueLabel}:\n" \
                                                               f"\tHEAP[(int)H] = 1;\n" \
                                                               f"\tH = H + 1;\n" \
                                                               f"\tgoto {lbla};\n" \
                                                               f"\t{valor_2.falseLabel}:\n" \
                                                               f"\tHEAP[(int)H] = 0;\n" \
                                                               f"\tH = H + 1;\n" \
                                                               f"\t{lbla}:\n"

                                codigo += f"\t{lbl10}:\n\n"
                                # ! Generar código para cambio de referencia
                                codigo += f"\tSTACK[(int){tmpd}] = {tmp1}; // Cambio de referencia\n"
                                # ! Retornar código
                                return codigo
                            else:
                                print("Se esperaba un dato de tipo 'USIZE' y se encontro '{}'.".format(valor_1.tipo[0].value))

                        else:
                            print("Error en las expresiones.")

                    # ! REMOVE
                    else:
                        # ! Traducir la expresión y obtener el dato resultante
                        valor_1 = self.exp1.convertir(generador, entorno)
                        # ! Validar que no haya ocurrido un error en la expresión al calcular el dato (None)
                        if valor_1:
                            # ! Validar que el dato sea de tipo I64
                            if valor_1.tipo[0] == TipoPrimitivo.I64:
                                # ! Verificar depth
                                if depth == 0:
                                    # ! Verificar si es referencia
                                    if variable.flag_reference:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* REMOVE() */\n" + valor_1.codigo + f"\t{tmp1} = S + {variable.posicion}; // Ref.\n" \
                                                                                          f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. variable\n" \
                                                                                          f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp2
                                        tmpv = tmp3
                                    else:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* REMOVE() */\n" + valor_1.codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                                                                          f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp1
                                        tmpv = tmp2
                                else:
                                    # ! Verificar si es referencia
                                    if variable.flag_reference:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        tmp4 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* REMOVE() */\n" + valor_1.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                          f"\t{tmp2} = {tmp1} + {variable.posicion}; // Ref.\n" \
                                                                                          f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. variable\n" \
                                                                                          f"\t{tmp4} = STACK[(int){tmp3}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp3
                                        tmpv = tmp4
                                    else:
                                        # ! Temporales auxiliares
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()
                                        # ! Crear código a retornar
                                        codigo = f"\t/* REMOVE() */\n" + valor_1.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                          f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                                                                          f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                        # ! Temporales de dirección
                                        tmpd = tmp2
                                        tmpv = tmp3
                                # ! Temporales auxiliares
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                tmp3 = generador.nuevoTemp()
                                tmp4 = generador.nuevoTemp()
                                tmp5 = generador.nuevoTemp()
                                tmp6 = generador.nuevoTemp()
                                tmp7 = generador.nuevoTemp()
                                tmp8 = generador.nuevoTemp()
                                tmp9 = generador.nuevoTemp()
                                tmp10 = generador.nuevoTemp()
                                # ! Etiquetas auxiliares
                                lbl1 = generador.nuevoLabel()
                                lbl2 = generador.nuevoLabel()
                                lbl3 = generador.nuevoLabel()
                                lbl4 = generador.nuevoLabel()
                                lbl5 = generador.nuevoLabel()
                                # ! Generar código
                                codigo += f"\t{tmp1} = H; // Nueva referencia\n\n" \
                                          f"\t// Migrar len\n" \
                                          f"\t{tmp2} = {tmpv} + 0; // Dir. len anterior\n" \
                                          f"\t{tmp3} = HEAP[(int){tmp2}]; // len anterior\n" \
                                          f"\t{tmp4} = {tmp3} - 1; // len anterior - 1\n" \
                                          f"\tHEAP[(int)H] = {tmp4};\n" \
                                          f"\tH = H + 1;\n\n" \
                                          f"\t// Migrar capacity\n" \
                                          f"\t{tmp5} = {tmpv} + 1; // Dir. capacity anterior\n" \
                                          f"\t{tmp6} = HEAP[(int){tmp5}]; // capacity anterior\n" \
                                          f"\tHEAP[(int)H] = {tmp6};\n" \
                                          f"\tH = H + 1;\n\n" \
                                          f"\t// Migrar valores\n" \
                                          f"\t{tmp7} = 0; // i\n" \
                                          f"\t{lbl5}:\n" \
                                          f"\tif ({tmp7} < {tmp3}) goto {lbl1}; // i < len anterior\n" \
                                          f"\tgoto {lbl2};\n" \
                                          f"\t{lbl1}:\n" \
                                          f"\t{tmp8} = {tmpv} + 2; // Pivote de valores\n" \
                                          f"\t{tmp9} = {tmp8} + {tmp7}; // Dir. valor\n" \
                                          f"\t{tmp10} = HEAP[(int){tmp9}]; // valor\n\n" \
                                          f"\tif ({tmp7} != {valor_1.reference}) goto {lbl3}; // i != indice remove\n" \
                                          f"\tgoto {lbl4};\n" \
                                          f"\t{lbl3}:\n" \
                                          f"\tHEAP[(int)H] = {tmp10};\n" \
                                          f"\tH = H + 1;\n" \
                                          f"\t{lbl4}:\n\n" \
                                          f"\t{tmp7} = {tmp7} + 1; // i++\n" \
                                          f"\tgoto {lbl5};\n" \
                                          f"\t{lbl2}:\n\n"
                                # ! Generar código para cambio de referencia
                                codigo += f"\tSTACK[(int){tmpd}] = {tmp1}; // Cambio de referencia\n"
                                # ! Retornar código
                                return codigo
                            else:
                                print("Se esperaba un dato de tipo 'USIZE' y se encontro '{}'.".format(valor_1.tipo[0].value))

                        else:
                            print("Error en la expresion.")

                else:
                    print("Se esperaba un dato de tipo 'VECTOR' y se encontro '{}'.".format(variable.tipo[0].value))

            else:
                print("No se puede cambiar el valor de una variable inmutable.")

        else:
            print("Variable '{}' no encontrada.".format(self.id))
