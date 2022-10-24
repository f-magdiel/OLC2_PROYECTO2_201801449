from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


class IfExpresion(Expresion):
    def __init__(self, fila, sentencias, else_expres=None):
        super().__init__(fila)
        self.sentencias = sentencias
        self.else_expres = else_expres

    def convertir(self, generador, entorno):
        # ! Crear el valor a retornar
        valor = Valor(self.fila, None)
        # ! Generar código inicial del valor
        valor.codigo = f"\t// Expresión IF\n"
        # ! Verificar si viene solo un if
        flag_unico = (len(self.sentencias) == 1) and (self.else_expres is None)
        # ! Bandera para encontrar el tipo del valor
        flag_tipo = True
        # ! Recorrer las sentencias
        for sentencia in self.sentencias:

            # ! Traducir la expresión de la condición y obtener el valor resultante
            val_cond = sentencia['exp1'].convertir(generador, entorno)
            # ! Validar que no haya ocurrido un error al traducir la expresión
            if val_cond:
                # ! Validar que el valor de la condición sea de tipo BOOL
                if val_cond.tipo[0] == TipoPrimitivo.BOOL:
                    # ! Traducir la expresión a asignar y obtener el valor resultante
                    val_asig = sentencia['exp2'].convertir(generador, entorno)
                    # ! Validar que no haya ocurrido un error al traducir la expresión

                    if val_asig:

                        # ! Verificar bandera de encontrar tipo
                        if flag_tipo:
                            # ! Cambiar bandera
                            flag_tipo = False
                            # ! Ajustar tipo
                            valor.tipo = val_asig.tipo
                            # ! Verificar el tipo
                            if valor.tipo[0] != TipoPrimitivo.BOOL:
                                # ! Generar temporal de referencia
                                valor.reference = generador.nuevoTemp()
                            else:
                                # ! Temporal del valor
                                tmpv = generador.nuevoTemp()
                        # ! Verificar el tipo
                        if val_asig.tipo[0] != TipoPrimitivo.BOOL:
                            # ! Generar código
                            valor.codigo += f"\t// Condición\n" + val_cond.codigo + \
                                            f"\t{val_cond.trueLabel}:\n" + val_asig.codigo + \
                                            f"\t{valor.reference} = {val_asig.reference};\n\n"
                            # ! Verificar si no viene solo un if
                            if not flag_unico:
                                valor.codigo += f"\tgoto ETIQUETA_IF; // Salir del if\n"
                            # ! Colocar etiqueta falsa
                            valor.codigo += f"\t{val_cond.falseLabel}:\n\n"
                        else:
                            # ! Etiqueta auxiliar
                            lbl1 = generador.nuevoLabel()
                            # ! Generar código
                            valor.codigo += f"\t// Condición\n" + val_cond.codigo + \
                                            f"\t{val_cond.trueLabel}:\n" + val_asig.codigo + \
                                            f"\t{val_asig.trueLabel}:\n" \
                                            f"\t{tmpv} = 1;\n" \
                                            f"\tgoto {lbl1};\n" \
                                            f"\t{val_asig.falseLabel}:\n" \
                                            f"\t{tmpv} = 0;\n" \
                                            f"\t{lbl1}:\n\n"
                            # ! Verificar si no viene solo un if
                            if not flag_unico:
                                valor.codigo += f"\tgoto ETIQUETA_IF; // Salir del if\n"
                            # ! Colocar etiqueta falsa
                            valor.codigo += f"\t{val_cond.falseLabel}:\n\n"
                    else:
                        alert = "Error en la expresion interna if expresion"
                        List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

                else:
                    alert = "La condicion debe ser de tipo 'BOOL'"
                    List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

            else:
                alert = "Error en la condicion if expresion."
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

        # ! Verificar si viene un else
        if self.else_expres:
            # ! Traducir la expresión a asignar y obtener el valor resultante
            val_asig = self.else_expres.convertir(generador, entorno)
            # ! Validar que no haya ocurrido un error al traducir la expresión
            if val_asig:
                # ! Verificar el tipo
                if val_asig.tipo[0] != TipoPrimitivo.BOOL:
                    # ! Generar código
                    valor.codigo += val_asig.codigo + f"\t{valor.reference} = {val_asig.reference};\n\n"
                else:
                    # ! Etiqueta auxiliar
                    lbl1 = generador.nuevoLabel()
                    # ! Generar código
                    valor.codigo += val_asig.codigo + f"\t{val_asig.trueLabel}:\n" \
                                                      f"\t{tmpv} = 1;\n" \
                                                      f"\tgoto {lbl1};\n" \
                                                      f"\t{val_asig.falseLabel}:\n" \
                                                      f"\t{tmpv} = 0;\n" \
                                                      f"\t{lbl1}:\n\n"
            else:
                alert = "Error en la expresion interna"
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

        # ! Verificar si no viene solo un if
        if not flag_unico:
            # ! Obtener etiqueta de salida
            lbl1 = generador.nuevoLabel()
            # ! Remplazar etiqueta de salida
            valor.codigo = valor.codigo.replace("ETIQUETA_IF", lbl1)
            # ! Colocar etiqueta de salida
            valor.codigo += f"\t{lbl1}:\n\n"
        # ! Verificar si es booleano

        if valor.tipo[0] == TipoPrimitivo.BOOL:
            # ! Generar etiquetas booleanas
            valor.trueLabel = generador.nuevoLabel()
            valor.falseLabel = generador.nuevoLabel()
            # ! Generar código
            valor.codigo += f"\tif ({tmpv}) goto {valor.trueLabel};\n" \
                            f"\tgoto {valor.falseLabel};\n"
        # ! Retornar el valor
        return valor
