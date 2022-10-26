from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Return(Instruccion):
    def __init__(self, fila, expresion):
        super().__init__(fila)
        self.expresion = expresion

    def convertir(self, generador, entorno):
        # ! Traducir la expresión y obtener el dato resultante
        valor = self.expresion.convertir(generador, entorno)
        # ! Validar que no haya ocurrido un error en la expresión al calcular el dato (None)
        if valor:
            # ! Obtener la variable return y la depth
            var_ret, depth = entorno.obtener_variable('return')

            # ! Validar si no es booleano
            if valor.tipo[0] != TipoPrimitivo.BOOL:
                # ! Verificar depth
                if depth == 0:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t// RETURN \n" + valor.codigo + f"\t{tmp1} = S + {var_ret.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp1}] = {valor.reference}; \n\n" \
                                                                  f"\t{tmp2} = S - TEMPORAL_RETURN;\n" \
                                                                  f"\tS = S - {tmp2};\n" \
                                                                  f"\tgoto ETIQUETA_RETURN; \n"
                else:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    # ! Generar código
                    codigo = f"\t// RETURN \n" + valor.codigo + f"\t{tmp1} = S - {depth}; \n" \
                                                                  f"\t{tmp2} = {tmp1} + {var_ret.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp2}] = {valor.reference}; \n\n" \
                                                                  f"\t{tmp3} = S - TEMPORAL_RETURN;\n" \
                                                                  f"\tS = S - {tmp3};\n" \
                                                                  f"\tgoto ETIQUETA_RETURN; \n"
            else:
                # ! Verificar depth
                if depth == 0:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    # ! Labels auxiliares
                    lbl1 = generador.nuevoLabel()
                    # ! Generar código
                    codigo = f"\t// RETURN \n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                  f"\t{tmp1} = S + {var_ret.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp1}] = 1; \n" \
                                                                  f"\tgoto {lbl1};\n" \
                                                                  f"\t{valor.falseLabel}:\n" \
                                                                  f"\t{tmp1} = S + {var_ret.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp1}] = 0; \n" \
                                                                  f"\t{lbl1}:\n\n" \
                                                                  f"\t{tmp2} = S - TEMPORAL_RETURN;\n" \
                                                                  f"\tS = S - {tmp2};\n" \
                                                                  f"\tgoto ETIQUETA_RETURN; \n"
                else:
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    # ! Labels auxiliares
                    lbl1 = generador.nuevoLabel()
                    # ! Generar código
                    codigo = f"\t// RETURN \n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                  f"\t{tmp1} = S - {depth}; \n" \
                                                                  f"\t{tmp2} = S + {var_ret.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp2}] = 1; \n" \
                                                                  f"\tgoto {lbl1};\n" \
                                                                  f"\t{valor.falseLabel}:\n" \
                                                                  f"\t{tmp1} = S - {depth}; \n" \
                                                                  f"\t{tmp2} = S + {var_ret.posicion}; \n" \
                                                                  f"\tSTACK[(int){tmp2}] = 0; \n" \
                                                                  f"\t{lbl1}:\n\n" \
                                                                  f"\t{tmp3} = S - TEMPORAL_RETURN;\n" \
                                                                  f"\tS = S - {tmp3};\n" \
                                                                  f"\tgoto ETIQUETA_RETURN; \n"
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
            alert = "Error en la expresion en RETURN"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
