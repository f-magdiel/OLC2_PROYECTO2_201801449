class Generador:
    def __init__(self):
        self.temporal = 1
        self.label = 1
        self.funciones_predef = []
        self.codigo = []
        self.tempLista = []
        self.generador_funciones()

    # ! funciones predeterminadas
    def generador_funciones(self):
        # ! creando temporales para su uso posterior
        tmp1 = self.nuevoTemp()
        tmp2 = self.nuevoTemp()
        tmp3 = self.nuevoTemp()
        tmp4 = self.nuevoTemp()

        # ! creando labels para su uso posterior
        lbl1 = self.nuevoLabel()
        lbl2 = self.nuevoLabel()
        lbl3 = self.nuevoLabel()

        codigo = "void imprimir(){\n" \
                 f"    // OBTENER DIRECCIÓN\n" \
                 f"    {tmp1} = SP + 0;\n" \
                 f"    {tmp2} = STACK[(int){tmp1}];\n" \
                 f"    // WHILE\n" \
                 f"    {lbl3}:\n" \
                 f"        // EXPRESIONES DE LA CONDICIÓN\n" \
                 f"        {tmp3} = HEAP[(int){tmp2}];\n" \
                 f"        {tmp4} = - 1;\n" \
                 f"        // CONDICIÓN\n" \
                 f"        if ({tmp3} != {tmp4}) goto {lbl1};\n" \
                 f"        goto {lbl2};\n" \
                 f"        {lbl1}:\n" \
                 f"            // IMPRIMIR CARÁCTER\n" \
                 f"            printf(\"%c\", (int){tmp3});\n" \
                 f"            {tmp2} = {tmp2} + 1;\n" \
                 f"        goto {lbl3};\n" \
                 f"        {lbl2}:\n" \
                 f"    return;\n" \
                 "}"
        self.funciones_predef.append(codigo)

        # ! temporales para uso en concatenar
        tmp1 = self.nuevoTemp()
        tmp2 = self.nuevoTemp()
        tmp3 = self.nuevoTemp()
        tmp4 = self.nuevoTemp()
        tmp5 = self.nuevoTemp()
        tmp6 = self.nuevoTemp()
        tmp7 = self.nuevoTemp()
        tmp8 = self.nuevoTemp()

        # ! labesl para uso en concatenar
        lbl1 = self.nuevoLabel()
        lbl2 = self.nuevoLabel()
        lbl3 = self.nuevoLabel()
        lbl4 = self.nuevoLabel()
        lbl5 = self.nuevoLabel()
        lbl6 = self.nuevoLabel()

        codigo = "void concatenar(){\n" \
                 f"    // OBTENER DIRECCIONES\n" \
                 f"    {tmp1} = SP + 0;\n" \
                 f"    {tmp2} = STACK[(int){tmp1}];\n" \
                 f"    {tmp3} = SP + 1;\n" \
                 f"    {tmp4} = STACK[(int){tmp3}];\n" \
                 f"    // WHILE CAD_1\n" \
                 f"    {lbl3}:\n" \
                 f"        // EXPRESIONES DE LA CONDICIÓN\n" \
                 f"        {tmp5} = HEAP[(int){tmp2}];\n" \
                 f"        {tmp6} = - 1;\n" \
                 f"        // CONDICIÓN\n" \
                 f"        if ({tmp5} != {tmp6}) goto {lbl1};\n" \
                 f"        goto {lbl2};\n" \
                 f"        {lbl1}:\n" \
                 f"            // CONCATENAR EN HEAP\n" \
                 f"            HEAP[(int)HP] = {tmp5};\n" \
                 f"            HP = HP + 1;\n" \
                 f"            {tmp2} = {tmp2} + 1;\n" \
                 f"        goto {lbl3};\n" \
                 f"        {lbl2}:\n" \
                 f"    // WHILE CAD_2\n" \
                 f"    {lbl6}:\n" \
                 f"        // EXPRESIONES DE LA CONDICIÓN\n" \
                 f"        {tmp7} = HEAP[(int){tmp4}];\n" \
                 f"        {tmp8} = - 1;\n" \
                 f"        // CONDICIÓN\n" \
                 f"        if ({tmp7} != {tmp8}) goto {lbl4};\n" \
                 f"        goto {lbl5};\n" \
                 f"        {lbl4}:\n" \
                 f"            // CONCATENAR EN HEAP\n" \
                 f"            HEAP[(int)HP] = {tmp7};\n" \
                 f"            HP = HP + 1;\n" \
                 f"            {tmp4} = {tmp4} + 1;\n" \
                 f"        goto {lbl6};\n" \
                 f"        {lbl5}:\n" \
                 f"    // COLOCAR FIN DE CADENA\n" \
                 f"    HEAP[(int)HP] = - 1;\n" \
                 f"    HP = HP + 1;\n" \
                 f"    return;\n" \
                 "}"
        self.funciones_predef.append(codigo)

    # ! Se obtiene los temporales usados
    def obtenerUsadoTemp(self):
        return ",".join(self.tempLista)

    def obtenerCodigo(self):
        codigoTemp = "/* ENCABEZADO */\n" \
                     "#include <stdio.h>\n" \
                     "#include <math.h>\n" \
                     "double HEAP[80000];\n" \
                     "double STACK[80000];\n" \
                     "double SP;\n" \
                     "double HP;\n\n"

        codigoTemp += "/* TEMPORALES */\n" + "double " + ",".join(self.tempLista) + ";\n\n"

        codigoTemp += "/* VARIABLES GLOBALES */\n" + "double i;\n\n"

        codigoTemp += "/* FUNCIONES */\n" + "\n\n".join(self.funciones_predef) + "\n\n"

        codigoTemp += "void main(){\n" + "\n".join(self.codigo) + "\n\n\treturn;\n}\n"

        return codigoTemp

    # ! Genera un nuevo temporal
    def nuevoTemp(self):
        temp = "t" + str(self.temporal)
        self.temporal = self.temporal + 1

        self.tempLista.append(temp)
        return temp

    # ! Genera un nuevo label
    def nuevoLabel(self):
        temp = self.label
        self.label = self.label + 1
        return "L" + str(temp)

    # def agregarLlamadaFuncion(self, nombre):
    #     self.codigo.append(nombre + "();")
    #
    # def agregarLabel(self, label):
    #     self.codigo.append(label + ":")
    #
    # def agregarExpresion(self, target, left, right, operador):
    #     self.codigo.append(target + " = " + left + " " + operador + " " + right + ";")
    #
    # def agregarIf(self, left, right, operador, label):
    #     self.codigo.append("if(" + left + " " + operador + " " + right + ") goto " + label + ";")
    #
    # def agregarGoto(self, label):
    #     self.codigo.append("goto " + label + ";")
    #
    # def agregarPrintf(self, tipo, valor):
    #     self.codigo.append("printf(\"%" + tipo + "\"," + valor + ");")
    #
    # def agregarSaltoLinea(self):
    #     self.codigo.append("printf(\"%c\",10;")
    #
    # def sigHeap(self,):
    #     self.codigo.append("P = P + 1 ;")
    #
    # def antHeap(self,):
    #     self.codigo.append("P = P - 1 ;")
    #
    # def obtenerValorHeap(self, target, index):
    #     self.codigo.append(target + "= HEAP[(int)" + index + "];")
    #
    # def agregarValorHeap(self, index, valor):
    #     self.codigo.append("HEAP[(int)" + index + "] = " + valor + ";")
    #
    # def obtenerValorStack(self, target, index):
    #     self.codigo.append(target + " = STACK[(int)" + index + "];")
    #
    # def agregarValorStack(self, index, valor):
    #     self.codigo.append("STACK[(int)" + index + "] = " + valor + ";")
