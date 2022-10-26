from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from Entorno.Variable import Variable
from General.General import Env_General
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class Forin(Instruccion):
    def __init__(self, fila, id, exp1, instrucciones, exp2=None):
        super().__init__(fila)
        self.id = id
        self.exp1 = exp1
        self.instrucciones = instrucciones
        self.exp2 = exp2

    def convertir(self, generador, entorno):
        valor1 = self.exp1.convertir(generador, entorno)
        if valor1:
            if self.exp2:
                valor2 = self.exp2.convertir(generador, entorno)
                if valor2:
                    if valor1.tipo[0] == TipoPrimitivo.I64 and valor2.tipo[0] == TipoPrimitivo.I64:
                        env_forin = Entorno(entorno, flag_bucle=True)
                        Env_General.append(env_forin)

                        indice = Variable(self.fila, self.id, True, [TipoPrimitivo.I64])
                        env_forin.nueva_variable(indice)

                        codigo = ""

                        for instruc in self.instrucciones:
                            if isinstance(instruc, Break) and not env_forin.flag_bucle:
                                print("Error invalido en entorno while")
                            elif isinstance(instruc, Continue) and not env_forin.flag_bucle:
                                print("Error invalido en entorno while")
                            else:
                                code = instruc.convertir(generador, env_forin)
                                if code:
                                    codigo += code + "\n"

                        # ! Temporales aux
                        tmp0 = generador.nuevoTemp()
                        tmp1 = generador.nuevoTemp()
                        tmp2 = generador.nuevoTemp()
                        tmp3 = generador.nuevoTemp()
                        tmp4 = generador.nuevoTemp()
                        tmp5 = generador.nuevoTemp()
                        tmp6 = generador.nuevoTemp()
                        tmp7 = generador.nuevoTemp()

                        lbl1 = generador.nuevoLabel()
                        lbl2 = generador.nuevoLabel()
                        lbl3 = generador.nuevoLabel()

                        codigo = f"\t// FORIN \n" + valor1.codigo + valor2.codigo + \
                                 f"\t \n" \
                                 f"\t{tmp0} = S;\n" \
                                 f"\t \n" \
                                 f"\tS = S + {entorno.size};\n\n" \
                                 f"\t \n" \
                                 f"\t{tmp1} = S + {indice.posicion}; \n" \
                                 f"\tSTACK[(int){tmp1}] = {valor1.reference}; \n\n" \
                                 f"\t{lbl3}:\n" \
                                 f"\t \n" \
                                 f"\t{tmp2} = S + {indice.posicion}; \n" \
                                 f"\t{tmp3} = STACK[(int){tmp2}]; \n" \
                                 f"\tif ({tmp3} < {valor2.reference}) goto {lbl1};\n" \
                                 f"\tgoto {lbl2};\n" \
                                 f"\t{lbl1}:\n\n" + codigo

                        if codigo.count("ETIQUETA_CONTINUE") > 0:
                            lbl4 = generador.nuevoLabel()
                            # ! Reemplazar etiquetas
                            codigo = codigo.replace("TEMPORAL_CONTINUE", tmp0)
                            codigo = codigo.replace("ETIQUETA_CONTINUE", lbl4)
                            # ! Generar código
                            codigo += f"\t{lbl4}:\n"

                        codigo += f"\t \n" \
                                  f"\t{tmp4} = S + {indice.posicion}; \n" \
                                  f"\t{tmp5} = STACK[(int){tmp4}]; \n" \
                                  f"\t{tmp6} = {tmp5} + 1; \n" \
                                  f"\t{tmp7} = S + {indice.posicion}; \n" \
                                  f"\tSTACK[(int){tmp7}] = {tmp6}; \n\n" \
                                  f"\t \n" \
                                  f"\tgoto {lbl3};\n\n" \
                                  f"\t{lbl2}:\n" \
                                  f"\t \n" \
                                  f"\tS = S - {entorno.size};\n"

                        if codigo.count("ETIQUETA_BREAK") > 0:
                            # ! Obtener etiqueta de salida
                            lbl2 = generador.nuevoLabel()
                            # ! Reemplazar etiquetas
                            codigo = codigo.replace("TEMPORAL_BREAK", tmp0)
                            codigo = codigo.replace("ETIQUETA_BREAK", lbl2)
                            # ! Agregar etiqueta al final
                            codigo += f"\t{lbl2}:\n"

                        if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
                            # ! Obtener etiqueta de salida
                            lbl1 = generador.nuevoLabel()
                            # ! Reemplazar etiquetas
                            codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
                            # ! Agregar etiqueta al final
                            codigo += f"\t{lbl1}:\n"

                        return codigo
                    else:
                        alert = "Error en FORIN por datos incompatibles"
                        List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                else:
                    alert = "Error en la expresion en FORIN"
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
            else:
                # ! Cuando no viene expresion 2
                if valor1.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                    if len(valor1.tipo) > 1:
                        if valor1.tipo[0] == TipoPrimitivo.ARREGLO:
                            v = 1
                        else:
                            v = 2

                        env_forin = Entorno(entorno, flag_bucle=True)
                        Env_General.append(env_forin)

                        dato = Variable(self.fila, self.id, True, valor1.tipo[1:])
                        env_forin.nueva_variable(dato)

                        codigo = ""

                        for instruc in self.instrucciones:
                            if isinstance(instruc, Break) and not env_forin.flag_bucle:
                                print("Error invalido en entorno while")
                            elif isinstance(instruc, Continue) and not env_forin.flag_bucle:
                                print("Error invalido en entorno while")
                            else:
                                code = instruc.convertir(generador, env_forin)
                                if code:
                                    codigo += code + "\n"

                        # ! Temporales aux
                        tmp1 = generador.nuevoTemp()
                        tmp2 = generador.nuevoTemp()
                        tmp3 = generador.nuevoTemp()
                        tmp4 = generador.nuevoTemp()
                        tmp5 = generador.nuevoTemp()
                        tmp6 = generador.nuevoTemp()
                        tmp7 = generador.nuevoTemp()
                        tmp8 = generador.nuevoTemp()

                        # ! Labels aux
                        lbl1 = generador.nuevoLabel()
                        lbl2 = generador.nuevoLabel()
                        lbl3 = generador.nuevoLabel()

                        codigo = f"\t// FORIN \n" + valor1.codigo + \
                                 f"\t \n" \
                                 f"\t{tmp1} = S;\n" \
                                 f"\t \n" \
                                 f"\tS = S + {entorno.size};\n\n" \
                                 f"\t \n" \
                                 f"\t{tmp2} = 0; \n\n" \
                                 f"\t{lbl3}:\n" \
                                 f"\t \n" \
                                 f"\t{tmp3} = {valor1.reference} + 0; \n" \
                                 f"\t{tmp4} = HEAP[(int){tmp3}]; \n" \
                                 f"\tif ({tmp2} < {tmp4}) goto {lbl1}; \n" \
                                 f"\tgoto {lbl2};\n" \
                                 f"\t{lbl1}:\n" \
                                 f"\t \n" \
                                 f"\t{tmp5} = {valor1.reference} + {v}; \n" \
                                 f"\t{tmp6} = {tmp5} + {tmp2}; \n" \
                                 f"\t{tmp7} = HEAP[(int){tmp6}]; \n\n" \
                                 f"\t \n" \
                                 f"\t{tmp8} = S + {dato.posicion}; \n" \
                                 f"\tSTACK[(int){tmp8}] = {tmp7}; \n\n" + codigo

                        if codigo.count("ETIQUETA_CONTINUE") > 0:
                            lbl4 = generador.nuevoLabel()
                            # ! Reemplazar etiquetas
                            codigo = codigo.replace("TEMPORAL_CONTINUE", tmp1)
                            codigo = codigo.replace("ETIQUETA_CONTINUE", lbl4)
                            # ! Generar código
                            codigo += f"\t{lbl4}:\n"

                        codigo += f"\t \n" \
                                  f"\t{tmp2} = {tmp2} + 1; \n\n" \
                                  f"\t \n" \
                                  f"\tgoto {lbl3};\n\n" \
                                  f"\t{lbl2}:\n" \
                                  f"\t \n" \
                                  f"\tS = S - {entorno.size};\n"

                        if codigo.count("ETIQUETA_BREAK") > 0:
                            # ! Obtener etiqueta de salida
                            lbl2 = generador.nuevoLabel()
                            # ! Reemplazar etiquetas
                            codigo = codigo.replace("TEMPORAL_BREAK", tmp1)
                            codigo = codigo.replace("ETIQUETA_BREAK", lbl2)
                            # ! Agregar etiqueta al final
                            codigo += f"\t{lbl2}:\n"
                            # ! Retornar el código

                        if codigo.count("ETIQUETA_FUERA_LIMITE") > 0:
                            # ! Obtener etiqueta de salida
                            lbl1 = generador.nuevoLabel()
                            # ! Reemplazar etiquetas
                            codigo = codigo.replace("ETIQUETA_FUERA_LIMITE", lbl1)
                            # ! Agregar etiqueta al final
                            codigo += f"\t{lbl1}:\n"

                        return codigo
                    else:
                        alert = "Error en tipo expresion en FORIN"
                        List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
                else:
                    alert = "Error tipo de dato invalido ARREGLO o VECTOR"
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Error en expresiones en FORIN"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
