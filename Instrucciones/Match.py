from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from General.General import Env_General
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Match(Instruccion):
    def __init__(self, fila, expresion, brazos):
        super().__init__(fila)
        self.expresion = expresion
        self.brazos = brazos

    def convertir(self, generador, entorno):
        valor_p = self.expresion.convertir(generador, entorno)
        if valor_p:
            if valor_p.tipo[0] not in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                codigo = f"\t// MATCH \n"
                if valor_p.tipo[0] != TipoPrimitivo.BOOL:
                    codigo += valor_p.codigo
                else:
                    tmp1 = generador.nuevoTemp()
                    # ! Se genera código
                    codigo += f"\t \n" \
                              f"\t{tmp1} = 0;\n" + valor_p.codigo + \
                              f"\t{valor_p.trueLabel}:\n" \
                              f"\t{tmp1} = 1;\n" \
                              f"\t{valor_p.falseLabel}:\n\n"

                # ! Ir por brazos
                for br in self.brazos:
                    codigo += f"\t \n"
                    ult_falseLabel = None
                    list_trueLabel = ""
                    cond = ""
                    # ! Recorrer expresiones de brazo
                    for expres in br['exps']:
                        if ult_falseLabel:
                            cond += f"\t{ult_falseLabel}:\n"

                        if expres == "_":
                            trueLabel = generador.nuevoLabel()
                            falseLabel = generador.nuevoLabel()
                            # ! Se genera código
                            cond += f"\tif (1) goto {trueLabel};\n" \
                                    f"\tgoto {falseLabel};\n"

                            # ! Actulizar dato brazo
                            ult_falseLabel = falseLabel
                            list_trueLabel += f"\t{trueLabel}:\n"

                        else:
                            valor = expres.convertir(generador, entorno)
                            if valor:
                                if valor.tipo[0] not in [TipoPrimitivo.STR, TipoPrimitivo.BOOL, TipoPrimitivo.STRING]:
                                    codigo += valor.codigo
                                    trueLabel = generador.nuevoLabel()
                                    falseLabel = generador.nuevoLabel()

                                    cond += f"\tif ({valor_p.reference} == {valor.reference}) goto {trueLabel};\n" \
                                            f"\tgoto {falseLabel};\n"
                                    # ! Actualizar información del brazo
                                    ult_falseLabel = falseLabel
                                    list_trueLabel += f"\t{trueLabel};\n"

                                elif valor.tipo[0] == TipoPrimitivo.BOOL:
                                    tmp2 = generador.nuevoTemp()
                                    trueLabel = generador.nuevoLabel()
                                    falseLabel = generador.nuevoLabel()

                                    cond += f"\t{tmp2} = 0;\n" + valor.codigo + \
                                            f"\t{valor.trueLabel}:\n" \
                                            f"\t{tmp2} = 1;\n" \
                                            f"\t{valor.falseLabel}:\n\n" \
                                            f"\tif ({tmp1} == {tmp2}) goto {trueLabel};\n" \
                                            f"\tgoto {falseLabel};\n"
                                    # ! Actualizar información del brazo
                                    ult_falseLabel = falseLabel
                                    list_trueLabel += f"\t{trueLabel}:\n"
                                else:
                                    codigo += valor.codigo

                                    # ! Temporales aux
                                    tmp1 = generador.nuevoTemp()
                                    tmp2 = generador.nuevoTemp()
                                    tmp3 = generador.nuevoTemp()
                                    tmp4 = generador.nuevoTemp()
                                    tmp5 = generador.nuevoTemp()
                                    tmp6 = generador.nuevoTemp()

                                    # ! Labels aux
                                    lbl1 = generador.nuevoLabel()
                                    lbl2 = generador.nuevoLabel()
                                    lbl3 = generador.nuevoLabel()
                                    lbl4 = generador.nuevoLabel()
                                    lbl5 = generador.nuevoLabel()
                                    lbl6 = generador.nuevoLabel()
                                    lbl7 = generador.nuevoLabel()
                                    lbl8 = generador.nuevoLabel()

                                    trueLabel = generador.nuevoLabel()
                                    falseLabel = generador.nuevoLabel()

                                    cond += f"\t \n" \
                                            f"\t{tmp1} = {valor_p.reference};\n" \
                                            f"\t{tmp2} = {valor.reference};\n\n" \
                                            f"\t{tmp3} = 0; \n" \
                                            f"\t{tmp4} = - 1; \n" \
                                            f"\t{lbl7}:\n" \
                                            f"\t{tmp5} = HEAP[(int){tmp1}]; \n" \
                                            f"\t{tmp6} = HEAP[(int){tmp2}]; \n\n" \
                                            f"\tif ({tmp5} == {tmp6}) goto {lbl1};\n" \
                                            f"\tgoto {lbl2};\n" \
                                            f"\t{lbl1}: \n" \
                                            f"\tif ({tmp5} == {tmp4}) goto {lbl3};\n" \
                                            f"\tgoto {lbl4};\n" \
                                            f"\t{lbl3}: \n" \
                                            f"\tif ({tmp6} == {tmp4}) goto {lbl5};\n" \
                                            f"\tgoto {lbl6};\n" \
                                            f"\t{lbl5}:  \n" \
                                            f"\t{tmp3} = 1;\n" \
                                            f"\tgoto {lbl8};\n" \
                                            f"\t{lbl6}: \n" \
                                            f"\tgoto {lbl8};\n" \
                                            f"\t{lbl4}: \n" \
                                            f"\t{tmp1} = {tmp1} + 1;\n" \
                                            f"\t{tmp2} = {tmp2} + 1;\n" \
                                            f"\tgoto {lbl7};\n" \
                                            f"\t{lbl2}: \n" \
                                            f"\t{lbl8}:\n\n" \
                                            f"\tif ({tmp3}) goto {trueLabel};\n" \
                                            f"\tgoto {falseLabel};\n"

                                    # ! Actualizar información del brazo
                                    ult_falseLabel = falseLabel
                                    list_trueLabel += f"\t{trueLabel}:\n"
                            else:
                                alert = "Error en la coincidencia  de brazos"
                                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                    # ! Insertar condiciones
                    codigo += cond
                    codigo += list_trueLabel
                    if len(br['instrs']) > 1:
                        env_match = Entorno(entorno, entorno.flag_bucle)
                    else:
                        env_match = Entorno(entorno, entorno.flag_bucle)
                    # ! Se agrega entorno a la lista de env general
                    Env_General.append(env_match)
                    codigo += f"\t \n" \
                              f"\tS = S + {entorno.size};\n\n"

                    for instruc in br['instrs']:
                        if isinstance(instruc, Break) and not env_match.flag_bucle:
                            print("Error en entonro match")
                        elif isinstance(instruc, Continue) and not env_match.flag_bucle:
                            print("Error en entonro match")
                        else:
                            code = instruc.convertir(generador, env_match)
                            if code:
                                codigo += code + "\n"

                    # ! Generar código de cambio de ámbito
                    codigo += f"\t \n" \
                              f"\tS = S - {entorno.size};\n\n"
                    # ! Generar salto de salida
                    codigo += f"\tgoto ETIQUETA_MATCH;\n"
                    # ! Insertar etiqueta falsa
                    codigo += f"\t{ult_falseLabel}:\n"

                # ! Labels de salida
                lbl1 = generador.nuevoLabel()
                codigo = codigo.replace("ETIQUETA_MATCH", lbl1)
                # Colocar etiqueta de salida
                codigo += f"\t{lbl1}:\n"
                # Retornar código
                if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
                    # ! Obtener etiqueta de salida
                    lbl1 = generador.nuevoLabel()
                    # ! Reemplazar etiquetas
                    codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
                    # ! Agregar etiqueta al final
                    codigo += f"\t{lbl1}:\n"

                if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
                    # ! Obtener etiqueta de salida
                    lbl1 = generador.nuevoLabel()
                    # ! Reemplazar etiquetas
                    codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
                    # ! Agregar etiqueta al final
                    codigo += f"\t{lbl1}:\n"

                return codigo
            else:
                alert = "Solo se permite un tipo primitivo en el dato de prueba"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Error en expresion de MATCH"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
