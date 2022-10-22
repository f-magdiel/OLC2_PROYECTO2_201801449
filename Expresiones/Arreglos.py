from Abstracta.Expresion import Expresion
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Arreglo(Expresion):
    def __init__(self, fila, expresiones):
        super().__init__(fila)
        self.expresiones = expresiones

    def convertir(self, generador, entorno):
        # ! Validar expresiones
        if not self.expresiones:
            valor = Valor(self.fila, [TipoPrimitivo.ARREGLO])
            valor.reference = generador.nuevoTemp()
            tmp1 = generador.nuevoTemp()
            # ! Se genera código
            valor.codigo = f"\t// Arreglo\n" \
                           f"\t{valor.reference} = H; // ref\n" \
                           f"\tH = H + 1; // Reservar espacio\n" \
                           f"\t{tmp1} = {valor.reference} + 0;" \
                           f"\tHEAP[(int){tmp1}] = 0; // len\n\n"
            return valor
        else:
            valores = []
            for i in range(len(self.expresiones)):
                valores.append(self.expresiones[i].convertir(generador, entorno))

            # ! Validar que no venga vacio
            if None not in valores:
                tipo = valores[0].tipo
                flag_correcto = True
                for valor in valores:
                    if len(valor.tipo) == len(tipo):
                        # ! Recorrer tipos
                        for i in range(len(tipo)):
                            if valor.tipo[i] != tipo[i]:
                                flag_correcto = False
                                break
                        if not flag_correcto:
                            break
                    else:
                        flag_correcto = False
                        break

                if flag_correcto:
                    # ! Se actualiza el tipo
                    tipo.insert(0, TipoPrimitivo.ARREGLO)
                    # ! Se crea nuevo valor
                    valor = Valor(self.fila, tipo)
                    # ! Referencia
                    valor.reference = generador.nuevoTemp()
                    # ! Aux temp
                    tmp1 = generador.nuevoTemp()
                    # ! Se genera código
                    valor.codigo += f"\t// Arreglo\n" \
                                    f"\t{valor.reference} = H; // ref\n" \
                                    f"\tH = H + {len(valores) + 1}; // Reservar espacio\n" \
                                    f"\t{tmp1} = {valor.reference} + 0;\n" \
                                    f"\tHEAP[(int){tmp1}] = {len(valores)}; // len\n\n"

                    for i in range(len(valores)):
                        if tipo[1] == TipoPrimitivo.BOOL:
                            tmp1 = generador.nuevoTemp()
                            lbl1 = generador.nuevoLabel()

                            valor.codigo += f"\t// Elemento\n" + valores[i].codigo + \
                                            f"\t{valores[i].trueLabel}:\n" \
                                            f"\t{tmp1} = {valor.reference} + {i + 1};\n" \
                                            f"\tHEAP[(int){tmp1}] = 1;\n" \
                                            f"\tgoto {lbl1};\n" \
                                            f"\t{valores[i].falseLabel}:\n" \
                                            f"\t{tmp1} = {valor.reference} + {i + 1};\n" \
                                            f"\tHEAP[(int){tmp1}] = 0;\n" \
                                            f"\t{lbl1}:\n\n"
                        else:
                            tmp1 = generador.nuevoTemp()
                            valor.codigo += f"\t// Elemento\n" + valores[i].codigo + \
                                            f"\t{tmp1} = {valor.reference} + {i + 1};\n" \
                                            f"\tHEAP[(int){tmp1}] = {valores[i].reference};\n\n"

                    return valor
                else:
                    print("Error ")
            else:
                print("Error en valores")
