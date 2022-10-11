from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from General.General import Env_General
from Instrucciones.Imprimir import Imprimir
from Instrucciones.While import While
from Instrucciones.If import If


class Match(Instruccion):
    def __init__(self, fila, expresion, brazos):
        super().__init__(fila)
        self.expresion = expresion
        self.brazos = brazos

    def convertir(self, generador, entorno):
        valor_p = self.expresion.convertir(generador, entorno)
        if valor_p:
            if valor_p.tipo[0] not in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                codigo = f"\t/* SENTENCIA MATCH */\n"

                if valor_p.tipo[0] != TipoPrimitivo.BOOL:
                    codigo += valor_p.codigo
                else:
                    tmp1 = generador.nuevoTemp()
                    # ! Se genera código
                    codigo += f"\t// Comparando booleanos\n" \
                              f"\t{tmp1} = 0;\n" + valor_p.codigo + \
                              f"\t{valor_p.trueLabel}:\n" \
                              f"\t{tmp1} = 1;\n" \
                              f"\t{valor_p.falseLabel}:\n\n"

                # ! Ir por brazos
                for br in self.brazos:
                    codigo += f"\t// Brazo\n"
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
                                if valor.tipo[0] not in [TipoPrimitivo.STR, TipoPrimitivo.BOOL]:
                                    codigo += valor.codigo
                                    trueLabel = generador.nuevoLabel()
                                    falseLabel = generador.nuevoLabel()

                                    cond += f"\tif ({valor_p.reference} == {valor.reference}) goto {trueLabel};\n" \
                                            f"\tgoto {falseLabel};\n"
                                    # ! Actualizar información del brazo
                                    ult_falseLabel = falseLabel
                                    list_trueLabel += f"\t{trueLabel}:\n"

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

                                    cond += f"\t// Comparando cadenas\n" \
                                            f"\t{tmp1} = {valor_p.reference};\n" \
                                            f"\t{tmp2} = {valor.reference};\n\n" \
                                            f"\t{tmp3} = 0; // Bandera\n" \
                                            f"\t{tmp4} = - 1; // Para comparar fin\n" \
                                            f"\t{lbl7}:\n" \
                                            f"\t{tmp5} = HEAP[(int){tmp1}]; // char1\n" \
                                            f"\t{tmp6} = HEAP[(int){tmp2}]; // char2\n\n" \
                                            f"\tif ({tmp5} == {tmp6}) goto {lbl1};\n" \
                                            f"\tgoto {lbl2};\n" \
                                            f"\t{lbl1}: // Cad1 llego a fin?\n" \
                                            f"\tif ({tmp5} == {tmp4}) goto {lbl3};\n" \
                                            f"\tgoto {lbl4};\n" \
                                            f"\t{lbl3}: // Cad2 llego a fin?\n" \
                                            f"\tif ({tmp6} == {tmp4}) goto {lbl5};\n" \
                                            f"\tgoto {lbl6};\n" \
                                            f"\t{lbl5}: // Son iguales \n" \
                                            f"\t{tmp3} = 1;\n" \
                                            f"\tgoto {lbl8};\n" \
                                            f"\t{lbl6}: // No son iguales\n" \
                                            f"\tgoto {lbl8};\n" \
                                            f"\t{lbl4}: // Sig. char\n" \
                                            f"\t{tmp1} = {tmp1} + 1;\n" \
                                            f"\t{tmp2} = {tmp2} + 1;\n" \
                                            f"\tgoto {lbl7};\n" \
                                            f"\t{lbl2}: // No son iguales\n" \
                                            f"\t{lbl8}:\n\n" \
                                            f"\tif ({tmp3}) goto {trueLabel};\n" \
                                            f"\tgoto {falseLabel};\n"

                                    # ! Actualizar información del brazo
                                    ult_falseLabel = falseLabel
                                    list_trueLabel += f"\t{trueLabel}:\n"
                            else:
                                print("ERROR")
                    # ! Insetar condiciones
                    codigo += cond
                    codigo += list_trueLabel
                    if len(br['instrs']) > 1:
                        env_match = Entorno(entorno, entorno.flag_bucle)
                    else:
                        env_match = Entorno(entorno, entorno.flag_bucle)
                    # ! Se agrega entorno a la lista de env general
                    Env_General.append(env_match)
                    codigo += f"\t// Cambio de ámbito\n" \
                              f"\tS = S + {entorno.size};\n\n"

                    for instruc in br['instrs']:
                        if isinstance(instruc, Imprimir):
                            codigo += instruc.convertir(generador, env_match) + "\n"
                        elif isinstance(instruc, If):
                            codigo += instruc.convertir(generador, env_match) + "\n"
                        elif isinstance(instruc, While):
                            codigo += instruc.convertir(generador, env_match) + "\n"
                        else:
                            print("Error en entonro match")
                    # ! Generar código de cambio de ámbito
                    codigo += f"\t// Cambio de ámbito\n" \
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
                return codigo
            else:
                print("Solo se permite un tipo primitivo en el dato de prueba")
        else:
            print("Error en expresion")