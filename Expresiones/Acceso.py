from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Acceso(Expresion):
    def __init__(self, fila, id, indices=None):
        super().__init__(fila)
        self.id = id
        self.indices = indices
        self.flag_argumento = False

    def convertir(self, generador, entorno):
        if entorno.existe_variable(self.id):
            variable, depth = entorno.obtener_variable(self.id)

            if self.indices is None:
                # ! Se genera valor
                valor = Valor(self.fila, variable.tipo)
                # ! Validar depth
                if depth == 0:
                    # ! Validar bandera argumento
                    if self.flag_argumento:
                        # ! validar bandera reference
                        if variable.flag_reference:
                            # ! Se genera un tempora y valor.refence
                            tmp1 = generador.nuevoTemp()
                            valor.reference = generador.nuevoTemp()
                            # ! Se genera código
                            valor.codigo = f"\t// Acceso array (es_ref/argumento) \n" \
                                           f"\t{tmp1} = S + {variable.posicion}; // Dir. array\n" \
                                           f"\t{valor.reference} = STACK[(int){tmp1}]; // Ref.\n\n"
                        else:
                            # ! Se genera temporal de referencia
                            valor.reference = generador.nuevoTemp()
                            # ! Se genera código
                            valor.codigo = f"\t// Acceso array (argumento) \n" \
                                           f"\t{valor.reference} = S + {variable.posicion}; // Dir. array\n\n"
                    else:
                        # ! Validar si es referencia
                        if variable.flag_reference:
                            # ! Temporales y valor referencia
                            tmp1 = generador.nuevoTemp()
                            tmp2 = generador.nuevoTemp()
                            valor.reference = generador.nuevoTemp()
                            # ! Se genera código
                            valor.codigo = f"\t// Acceso array (es_ref) \n" \
                                           f"\t{tmp1} = S + {variable.posicion}; // Dir. array\n" \
                                           f"\t{tmp2} = STACK[(int){tmp1}]; // Ref.\n" \
                                           f"\t{valor.reference} = STACK[(int){tmp2}]; // Valor\n\n"

                        else:
                            # ! Validar el tipo
                            if variable.tipo[0] not in [TipoPrimitivo.BOOL, TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                                # ! Temporales y valor referenia
                                tmp1 = generador.nuevoTemp()
                                valor.reference = generador.nuevoTemp()
                                # ! Se genera código
                                valor.codigo = f"\t// Acceso variable\n" \
                                               f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                               f"\t{valor.reference} = STACK[(int){tmp1}]; // Valor\n\n"

                            elif variable.tipo[0] == TipoPrimitivo.BOOL:
                                # ! Temporales y label false, true
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                valor.trueLabel = generador.nuevoLabel()
                                valor.falseLabel = generador.nuevoLabel()

                                valor.codigo = f"\t// Acceso variable\n" \
                                               f"\t{tmp1} = S + {variable.posicion}; // Dir. variable\n" \
                                               f"\t{tmp2} = STACK[(int){tmp1}]; // Valor\n\n" \
                                               f"\tif ({tmp2}) goto {valor.trueLabel};\n" \
                                               f"\tgoto {valor.falseLabel};\n"
                            else:
                                # ! Temporales auxiliares
                                tmp1 = generador.nuevoTemp()
                                # ! Generar nuevo temporal de referencia
                                valor.reference = generador.nuevoTemp()
                                # ! Generar código
                                valor.codigo = f"\t// Acceso array (es_ref) \n" \
                                               f"\t{tmp1} = S + {variable.posicion}; // Dir. array\n" \
                                               f"\t{valor.reference} = STACK[(int){tmp1}]; // Valor\n\n"
                else:
                    # ! Validar si es argumento
                    if self.flag_argumento:
                        # ! Validar referencia
                        if variable.flag_reference:
                            # ! Temporales y valor referencia
                            tmp1 = generador.nuevoTemp()
                            tmp2 = generador.nuevoTemp()
                            valor.reference = generador.nuevoTemp()
                            # ! Se genera código
                            valor.codigo = f"\t// Acceso array (es_ref/argumento) \n" \
                                           f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                           f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. array\n" \
                                           f"\t{valor.reference} = STACK[(int){tmp2}]; // Ref.\n\n"
                        else:
                            # ! Temporales y valor referencia
                            tmp1 = generador.nuevoTemp()
                            valor.reference = generador.nuevoTemp()
                            # ! Se genera códgio
                            valor.codigo = f"\t// Acceso array (argumento) \n" \
                                           f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                           f"\t{valor.reference} = {tmp1} + {variable.posicion}; // Dir. array\n\n"

                    else:
                        # ! Validar referencia
                        if variable.flag_reference:
                            # ! Temporales y valor referencia
                            tmp1 = generador.nuevoTemp()
                            tmp2 = generador.nuevoTemp()
                            tmp3 = generador.nuevoTemp()
                            valor.reference = generador.nuevoTemp()
                            # ! Se genera código
                            valor.codigo = f"\t// Acceso array (es_ref) \n" \
                                           f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                           f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. array\n" \
                                           f"\t{tmp3} = STACK[(int){tmp2}]; // Ref.\n" \
                                           f"\t{valor.reference} = STACK[(int){tmp3}]; // Valor\n\n"
                        else:
                            # ! Validar el tipo
                            if variable.tipo[0] not in [TipoPrimitivo.BOOL, TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                                # ! Temporales y valor referencia
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                valor.reference = generador.nuevoTemp()
                                # ! Se generá código
                                valor.codigo = f"\t// Acceso variable\n" \
                                               f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                               f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                               f"\t{valor.reference} = STACK[(int){tmp2}]; // Valor\n\n"

                            elif variable.tipo[0] == TipoPrimitivo.BOOL:
                                # ! Temporales y valor referencia
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                tmp3 = generador.nuevoTemp()
                                valor.trueLabel = generador.nuevoLabel()
                                valor.falseLabel = generador.nuevoLabel()
                                # ! Se genera código
                                valor.codigo = f"\t// Acceso variable\n" \
                                               f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                               f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. variable\n" \
                                               f"\t{tmp3} = STACK[(int){tmp2}]; // Valor\n\n" \
                                               f"\tif ({tmp3}) goto {valor.trueLabel};\n" \
                                               f"\tgoto {valor.falseLabel};\n"
                            else:
                                # ! Temporales y valor referencia
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                valor.reference = generador.nuevoTemp()

                                valor.codigo = f"\t// Acceso array \n" \
                                               f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                               f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. array\n" \
                                               f"\t{valor.reference} = STACK[(int){tmp2}]; // Valor\n\n"
                return valor
            else:
                # ! Validar si var es tipo array
                if variable.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                    valores = []
                    for index in self.indices:
                        valores.append(index.convertir(generador, entorno))

                    # ! Validar que ninguno sea vacio
                    if None not in valores:
                        flag_correcto = True
                        for i in range(len(valores)):
                            if valores[i].tipo[0] != TipoPrimitivo.I64:
                                flag_correcto = False
                                break

                        # ! Validar bandera
                        if flag_correcto:
                            valor = Valor(self.fila, variable.tipo[len(self.indices):])
                            valor.codigo = f"\t// Acceso array (indices)\n"

                            if depth == 0:
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                # ! Se genera código
                                valor.codigo += f"\t{tmp1} = S + {variable.posicion}; // Dir. array\n" \
                                                f"\t{tmp2} = STACK[(int){tmp1}]; // Acceso 1\n"
                                tmp = tmp2
                            else:
                                # ! Temporales y valor referencia
                                tmp1 = generador.nuevoTemp()
                                tmp2 = generador.nuevoTemp()
                                tmp3 = generador.nuevoTemp()
                                # ! Se genera código
                                valor.codigo += f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. array\n" \
                                                f"\t{tmp3} = STACK[(int){tmp2}]; // Acceso 1\n"
                                tmp = tmp3
                            # ! Validar si es referencia
                            if variable.flag_reference:
                                tmp1 = generador.nuevoTemp()
                                valor.codigo += f"\t{tmp1} = STACK[(int){tmp}]; // Acceso 2\n"
                                tmp = tmp1

                            for i in range(len(valores)):
                                if variable.tipo[i] == TipoPrimitivo.ARREGLO:
                                    v = 1
                                else:
                                    v = 2

                                # ! Temporales
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
                                tmp12 = generador.nuevoTemp()

                                # ! Labels
                                lbl1 = generador.nuevoLabel()
                                lbl2 = generador.nuevoLabel()
                                lbl3 = generador.nuevoLabel()
                                lbl4 = generador.nuevoLabel()
                                lbl5 = generador.nuevoLabel()
                                lbl6 = generador.nuevoLabel()

                                # Generar código
                                valor.codigo += f"\n\t// Indice\n" + valores[i].codigo + \
                                                f"\t{tmp1} = {tmp} + {v}; // Pivote valores\n" \
                                                f"\t{tmp2} = {tmp1} + {valores[i].reference}; // Indice en C3D\n\n" \
                                                f"\t{tmp3} = {tmp} + 0; // Dir. len\n" \
                                                f"\t{tmp4} = HEAP[(int){tmp3}]; // len\n" \
                                                f"\tif ({valores[i].reference} < 0) goto {lbl1}; // indice < 0\n" \
                                                f"\tgoto {lbl2};\n" \
                                                f"\t{lbl2}:\n" \
                                                f"\tif ({valores[i].reference} >= {tmp4}) goto {lbl3}; // indice >= len\n" \
                                                f"\tgoto {lbl4};\n" \
                                                f"\t{lbl1}:\n" \
                                                f"\t{lbl3}:\n" \
                                                f"\tprintf(\"%c\", 66); //B\n" \
                                                f"\tprintf(\"%c\", 111); //o\n" \
                                                f"\tprintf(\"%c\", 117); //u\n" \
                                                f"\tprintf(\"%c\", 110); //n\n" \
                                                f"\tprintf(\"%c\", 100); //d\n" \
                                                f"\tprintf(\"%c\", 115); //s\n" \
                                                f"\tprintf(\"%c\", 69); //E\n" \
                                                f"\tprintf(\"%c\", 114); //r\n" \
                                                f"\tprintf(\"%c\", 114); //r\n" \
                                                f"\tprintf(\"%c\", 111); //o\n" \
                                                f"\tprintf(\"%c\", 114); //r\n" \
                                                f"\tprintf(\"%c\", 10);\n" \
                                                f"\tgoto ETIQUETA_FUERA_LIMITE;\n" \
                                                f"\t{lbl4}:\n"

                                # ! Validar si es el ultimo a acceder
                                if i == (len(valores) - 1):
                                    valor.codigo += "\n"
                                    tmp = tmp2

                                else:
                                    tmp1 = generador.nuevoTemp()
                                    valor.codigo += f"\n\t{tmp1} = HEAP[(int){tmp2}]; // Nuevo acceso\n\n"
                                    tmp = tmp1
                            # ! Validar el tipo a retornar
                            if valor.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                                if self.flag_argumento:
                                    valor.reference = tmp
                                else:
                                    valor.reference = generador.nuevoTemp()
                                    valor.codigo += f"\t// Acceso item array\n" \
                                                    f"\t{valor.reference} = HEAP[(int){tmp}]; // Valor\n\n"
                            else:
                                # ! Validar el tipo
                                if valor.tipo[0] != TipoPrimitivo.BOOL:
                                    valor.reference = generador.nuevoTemp()
                                    valor.codigo += f"\t// Acceso item array\n" \
                                                    f"\t{valor.reference} = HEAP[(int){tmp}]; // Valor\n\n"
                                else:
                                    # ! Temporales
                                    tmp1 = generador.nuevoTemp()
                                    valor.trueLabel = generador.nuevoLabel()
                                    valor.falseLabel = generador.nuevoLabel()
                                    valor.codigo = f"\t// Acceso item array\n" \
                                                   f"\t{tmp1} = HEAP[(int){tmp}]; // Valor\n\n" \
                                                   f"\tif ({tmp1}) goto {valor.trueLabel};\n" \
                                                   f"\tgoto {valor.falseLabel};\n"
                            return valor
                        else:
                            print("Error indices incorrectos")
                    else:
                        print("Error en los indices")
                else:
                    print("No se puede indexar un valor de tipo '{}'.".format(variable.tipo[0].value))
        else:
            print("Variable '{}' no encontrada.".format(self.id))
