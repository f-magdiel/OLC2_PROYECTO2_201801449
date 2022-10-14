from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo


class Asignacion(Instruccion):
    def __init__(self, fila, id, expresion, indices=None):
        super().__init__(fila)
        self.id = id
        self.expresion = expresion
        self.indices = indices


    def convertir(self, generador, entorno):
        if entorno.existe_variable(self.id):
            var, depth = entorno.obtener_variable(self.id)
            if var.mutable:
                valor = self.expresion.convertir(generador, entorno)
                if valor:
                    if self.indices is None:
                        return self.asignacion_val(generador, var, depth, valor)
                    else:
                        if var.tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                            valores = []
                            for indice in self.indices:
                                valores.append(indice.convertir(generador, entorno))

                            # ! Validar que un valor no sea vacio
                            if None not in valores:
                                flag_correcto = True
                                for i in range(len(valores)):
                                    if valores[i].tipo[0] != TipoPrimitivo.I64:
                                        flag_correcto = False
                                        break
                                if flag_correcto:
                                    if depth == 0:
                                        # ! Temporales aux
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()

                                        codigo = f"\t/* ASIGNACIÓN */\n" \
                                                 f"\t{tmp1} = S + {var.posicion}; // Dir. var\n" \
                                                 f"\t{tmp2} = STACK[(int){tmp1}]; // Dir. array\n\n"
                                        tmp = tmp2
                                    else:
                                        # ! Temporales aux
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()
                                        tmp3 = generador.nuevoTemp()

                                        codigo = f"\t/* ASIGNACIÓN */\n" \
                                                 f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                 f"\t{tmp2} = {tmp1} + {var.posicion}; // Dir. var\n" \
                                                 f"\t{tmp3} = STACK[(int){tmp2}]; // Dir. array\n\n"
                                        tmp = tmp3

                                    for i in range(len(valores)):
                                        if var.tipo[0] == TipoPrimitivo.ARREGLO:
                                            val = 1
                                        else:
                                            val = 2
                                        tmp1 = generador.nuevoTemp()
                                        tmp2 = generador.nuevoTemp()

                                        codigo += f"\t// Indice\n" + valores[i].codigo + \
                                                  f"\t{tmp1} = {tmp} + {val}; // Pivote valores\n" \
                                                  f"\t{tmp2} = {tmp1} + {valores[i].reference}; // Indice en C3D\n\n"

                                    return self.asignacion_arr(generador, codigo, tmp, valor)
                                else:
                                    print("Error")
                            else:
                                print("Error")
                        else:
                            print("Error")
                else:
                    print("Error")
            else:
                print("Error")
        else:
            print("Error en encontrar variable")

    def asignacion_val(self, generador, variable, depth, valor):
        if valor.tipo != TipoPrimitivo.BOOL:
            if depth:
                tmp1 = generador.nuevoTemp()
                codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S + {variable.posicion}; // Dir. var\n" \
                                                                  f"\tSTACK[(int){tmp1}] = {valor.reference}; // Asignar\n"
                # Retornar código
                return codigo
            else:
                # ! Temporales aux
                tmp1 = generador.nuevoTemp()
                tmp2 = generador.nuevoTemp()
                # ! Se genera código
                codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                  f"\t{tmp2} = {tmp1} + {variable.posicion}; // Dir. var\n" \
                                                                  f"\tSTACK[(int){tmp2}] = {valor.reference}; // Asignar\n"
                return codigo
        else:
            # ! Validar profundidad
            if depth:
                # ! Temporal y Label aux
                tmp1 = generador.nuevoTemp()
                lbl1 = generador.nuevoLabel()

                codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                  f"\t{tmp1} = S + {variable.posicion}; // Dir. var\n" \
                                                                  f"\tSTACK[(int){tmp1}] = 1; // Asignar\n" \
                                                                  f"\tgoto {lbl1};\nbl" \
                                                                  f"\t{valor.falseLabel}:\n" \
                                                                  f"\t{tmp1} = S + {variable.posicion}; // Dir. var\n" \
                                                                  f"\tSTACK[(int){tmp1}] = 0; // Asignar\n" \
                                                                  f"\t{lbl1}:\n"
                return codigo
            else:
                # ! Temporales  y Label aux
                tmp1 = generador.nuevoTemp()
                tmp2 = generador.nuevoTemp()
                lbl1 = generador.nuevoLabel()

                codigo = f"\t/* ASIGNACIÓN */\n" + valor.codigo + f"\t{valor.trueLabel}:\n" \
                                                                  f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                  f"\t{tmp2} = S + {variable.posicion}; // Dir. var\n" \
                                                                  f"\tSTACK[(int){tmp2}] = 1; // Asignar\n" \
                                                                  f"\tgoto {lbl1};\n" \
                                                                  f"\t{valor.falseLabel}:\n" \
                                                                  f"\t{tmp1} = S - {depth}; // Entorno pivote\n" \
                                                                  f"\t{tmp2} = S + {variable.posicion}; // Dir. var\n" \
                                                                  f"\tSTACK[(int){tmp2}] = 0; // Asignar\n" \
                                                                  f"\t{lbl1}:\n"

                return codigo

    def asignacion_arr(self, generador, codigo, dir, valor):
        if valor.tipo != TipoPrimitivo.BOOL:
            codigo += valor.codigo + f"\tSTACK[(int){dir}] = {valor.reference}; // Asignar\n"
            return codigo
        else:
            lbl1 = generador.nuevoLabel()
            codigo += valor.codigo + f"\t{valor.trueLabel}:\n" \
                                     f"\tSTACK[(int){dir}] = 1; // Asignar\n" \
                                     f"\tgoto {lbl1};\n" \
                                     f"\t{valor.falseLabel}:\n" \
                                     f"\tSTACK[(int){dir}] = 0; // Asignar\n" \
                                     f"\t{lbl1}:\n"
            return codigo
