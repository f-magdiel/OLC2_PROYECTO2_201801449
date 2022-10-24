from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Remove(Expresion):
    def __init__(self, fila, id, expresion):
        super().__init__(fila)
        self.id = id
        self.expresion = expresion

    def convertir(self, generador, entorno):
        # ! Validar si existe la variable en la tabla de símbolos
        if entorno.existe_variable(self.id):
            # ! Obtener la variable y la depth
            variable, depth = entorno.obtener_variable(self.id)
            # ! Validar si la variable es mutable o no
            if variable.mutable:
                # ! Validar si la variables es de tipo VECTOR
                if variable.tipo[0] == TipoPrimitivo.VECTOR:
                    # ! Traducir la expresión y obtener el valor resultante
                    valor_del = self.expresion.convertir(generador, entorno)
                    # ! Validar que no haya ocurrido un error en la expresión al calcular el valor (None)
                    if valor_del:
                        # ! Validar que el valor sea de tipo I64
                        if valor_del.tipo[0] == TipoPrimitivo.I64:
                            # ! Crear el valor a retornar
                            valor = Valor(self.fila, variable.tipo[1:])
                            # ! Verificar depth
                            if depth == 0:
                                # ! Verificar si es referencia
                                if variable.flag_reference:
                                    # ! Temporales auxiliares
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    tmp3 = generador.nuevoTemp()
                                    # ! Crear código a retornar
                                    valor.codigo = f"\t/* REMOVE() */\n" + valor_del.codigo + f"\t{tmp1} = S + {variable.posicion}; // Ref.\n" \
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
                                    valor.codigo = f"\t/* REMOVE() */\n" + valor_del.codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
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
                                    valor.codigo = f"\t/* REMOVE() */\n" + valor_del.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
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
                                    valor.codigo = f"\t/* REMOVE() */\n" + valor_del.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                                              f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                                                                              f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. vector\n\n"
                                    # ! Temporales de dirección
                                    tmpd = tmp2
                                    mpv = tmp3
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
                            tmp11 = generador.nuevoTemp()  # ! Valor remove
                            # ! Etiquetas auxiliares
                            lbl1 = generador.nuevoLabel()
                            lbl2 = generador.nuevoLabel()
                            lbl3 = generador.nuevoLabel()
                            lbl4 = generador.nuevoLabel()
                            lbl5 = generador.nuevoLabel()
                            lbl6 = generador.nuevoLabel()
                            # ! Generar código
                            valor.codigo += f"\t{tmp1} = H; // Nueva referencia\n\n" \
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
                                            f"\t{lbl6}:\n" \
                                            f"\tif ({tmp7} < {tmp3}) goto {lbl1}; // i < len anterior\n" \
                                            f"\tgoto {lbl2};\n" \
                                            f"\t{lbl1}:\n" \
                                            f"\t{tmp8} = {tmpv} + 2; // Pivote de valores\n" \
                                            f"\t{tmp9} = {tmp8} + {tmp7}; // Dir. valor\n" \
                                            f"\t{tmp10} = HEAP[(int){tmp9}]; // valor\n\n" \
                                            f"\tif ({tmp7} != {valor_del.reference}) goto {lbl3}; // i != indice remove\n" \
                                            f"\tgoto {lbl4};\n" \
                                            f"\t{lbl3}:\n" \
                                            f"\tHEAP[(int)H] = {tmp10};\n" \
                                            f"\tH = H + 1;\n" \
                                            f"\tgoto {lbl5};\n" \
                                            f"\t{lbl4}:\n" \
                                            f"\t{tmp11} = {tmp10}; // Valor remove\n" \
                                            f"\t{lbl5}:\n\n" \
                                            f"\t{tmp7} = {tmp7} + 1; // i++\n" \
                                            f"\tgoto {lbl6};\n" \
                                            f"\t{lbl2}:\n\n"
                            # ! Generar código para cambio de referencia
                            valor.codigo += f"\tSTACK[(int){tmpd}] = {tmp1}; // Cambio de referencia\n\n"
                            # ! Verificar el tipo a retornar
                            if valor.tipo[0] != TipoPrimitivo.BOOL:
                                # ! Asignar referencia
                                valor.reference = tmp11
                            else:
                                # ! Generar etiquetas booleanas
                                valor.trueLabel = generador.nuevoLabel()
                                valor.falseLabel = generador.nuevoLabel()
                                # ! Generar código
                                valor.codigo = f"\t// Acceso variable\n" \
                                               f"\tif ({tmp11}) goto {valor.trueLabel};\n" \
                                               f"\tgoto {valor.falseLabel};\n"
                            # ! Retornar el valor
                            return valor
                        else:
                            alert = "Se esperaba un valor de tipo 'USIZE' y se encontro '{}'.".format(valor_del.tipo[0].value)
                            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

                    else:
                        alert = "Error en la expresion remove "
                        List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

                else:
                    alert = "Se esperaba un valor de tipo 'VECTOR' y se encontro '{}'.".format(variable.tipo[0].value)
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

            else:
                alert = "No se puede cambiar el valor de una variable inmutable."
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

        else:
            alert = "Variable '{}' no fue encontrada".format(self.id)
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
