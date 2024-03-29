from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Entorno import Entorno
from General.General import Env_General
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class If(Instruccion):
    def __init__(self, fila, sentencias, else_ins=None):
        super().__init__(fila)
        self.sentencias = sentencias
        self.else_ins = else_ins

    def convertir(self, generador, entorno):
        # ! Convertir las sentencias
        valores = []
        for sent in self.sentencias:
            valores.append(sent['exp'].convertir(generador, entorno))
        # ! Validación de no haya error al convertir
        if None not in valores:
            # ! Que sean de tipo BOOL
            flag_correcto = True
            for valor in valores:
                if valor.tipo[0] != TipoPrimitivo.BOOL:
                    flag_correcto = False
                    break
            # ! QUe sean de tipo BOOL
            if flag_correcto:
                # ! Se genera código
                codigo = f"\t// IF \n"
                # ! Solo un if viene
                flag_uno = len(self.sentencias) == 1 and self.else_ins is None
                # ! Recorrer la lista de sentencias
                for i in range(len(valores)):
                    # ! Env de if
                    env_if = Entorno(entorno, entorno.flag_bucle)
                    # ! Se agrega entorno a la lista Env
                    Env_General.append(env_if)

                    # ! Se obtiene el valor
                    valor = valores[i]
                    # ! Se genera código
                    codigo += f"\t \n" + valor.codigo + \
                              f"\t{valor.trueLabel}:\n"
                    # ! Generar código de cambio de ámbito
                    codigo += f"\t \n" \
                              f"\tS = S + {entorno.size};\n\n"
                    # ! Se recorren las instrucciones
                    for instruc in self.sentencias[i]['instrs']:
                        # ! Solo permitidos
                        if isinstance(instruc, Break) and not env_if.flag_bucle:
                            print("Error instruccines invalida en entorno if")
                        elif isinstance(instruc, Continue) and not env_if.flag_bucle:
                            print("Error instruccines invalida en entorno if")
                        else:
                            code = instruc.convertir(generador, env_if)
                            if code:
                                codigo += code + "\n"

                    # ! Código para cambio de entorno
                    codigo += f"\t \n" \
                              f"\tS = S - {entorno.size};\n\n"

                    if not flag_uno:
                        codigo += f"\tgoto ETIQUETA_IF;\n"

                    codigo += f"\t{valor.falseLabel}:\n"

                if self.else_ins:
                    env_if = Entorno(entorno, entorno.flag_bucle)
                    Env_General.append(env_if)
                    # ! Se genera código
                    codigo += f"\t \n" \
                              f"\tS = S + {entorno.size};\n\n"
                    # ! Recorrer instrucciones
                    for instruc in self.else_ins:
                        if isinstance(instruc, Break) and not env_if.flag_bucle:
                            print("Error instruccines invalida en entorno if")
                        elif isinstance(instruc, Continue) and not env_if.flag_bucle:
                            print("Error instruccines invalida en entorno if")
                        else:
                            code = instruc.convertir(generador, env_if)

                            if code:
                                codigo += code + "\n"

                    # ! Código cambio de entorno
                    codigo += f"\t \n" \
                              f"\tS = S - {entorno.size};\n"

                if not flag_uno:
                    lbl1 = generador.nuevoLabel()
                    codigo = codigo.replace("ETIQUETA_IF", lbl1)
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
                alert = "Error no es tipo bool en IF"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
        else:
            alert = "Error en las condicionales del IF"
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
