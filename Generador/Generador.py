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
                 f"    \n" \
                 f"    {tmp1} = S + 0;\n" \
                 f"    {tmp2} = STACK[(int){tmp1}];\n" \
                 f"    \n" \
                 f"    {lbl3}:\n" \
                 f"        \n" \
                 f"        {tmp3} = HEAP[(int){tmp2}];\n" \
                 f"        {tmp4} = - 1;\n" \
                 f"        \n" \
                 f"        if ({tmp3} != {tmp4}) goto {lbl1};\n" \
                 f"        goto {lbl2};\n" \
                 f"        {lbl1}:\n" \
                 f"            \n" \
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
                 f"    \n" \
                 f"    {tmp1} = S + 0;\n" \
                 f"    {tmp2} = STACK[(int){tmp1}];\n" \
                 f"    {tmp3} = S + 1;\n" \
                 f"    {tmp4} = STACK[(int){tmp3}];\n" \
                 f"    \n" \
                 f"    {lbl3}:\n" \
                 f"        \n" \
                 f"        {tmp5} = HEAP[(int){tmp2}];\n" \
                 f"        {tmp6} = - 1;\n" \
                 f"        \n" \
                 f"        if ({tmp5} != {tmp6}) goto {lbl1};\n" \
                 f"        goto {lbl2};\n" \
                 f"        {lbl1}:\n" \
                 f"            \n" \
                 f"            HEAP[(int)H] = {tmp5};\n" \
                 f"            H = H + 1;\n" \
                 f"            {tmp2} = {tmp2} + 1;\n" \
                 f"        goto {lbl3};\n" \
                 f"        {lbl2}:\n" \
                 f"    \n" \
                 f"    {lbl6}:\n" \
                 f"        \n" \
                 f"        {tmp7} = HEAP[(int){tmp4}];\n" \
                 f"        {tmp8} = - 1;\n" \
                 f"        \n" \
                 f"        if ({tmp7} != {tmp8}) goto {lbl4};\n" \
                 f"        goto {lbl5};\n" \
                 f"        {lbl4}:\n" \
                 f"            \n" \
                 f"            HEAP[(int)H] = {tmp7};\n" \
                 f"            H = H + 1;\n" \
                 f"            {tmp4} = {tmp4} + 1;\n" \
                 f"        goto {lbl6};\n" \
                 f"        {lbl5}:\n" \
                 f"    \n" \
                 f"    HEAP[(int)H] = - 1;\n" \
                 f"    H = H + 1;\n" \
                 f"    return;\n" \
                 "}"
        self.funciones_predef.append(codigo)

    # ! Se obtiene los temporales usados
    def obtenerUsadoTemp(self):
        return ",".join(self.tempLista)

    def obtenerCodigo(self):
        codigoTemp = " \n" \
                     "#include <stdio.h>\n" \
                     "#include <math.h>\n" \
                     "double HEAP[80000];\n" \
                     "double STACK[80000];\n" \
                     "double S;\n" \
                     "double H;\n\n"

        codigoTemp += "// TMP \n" + "double " + ",".join(self.tempLista) + ";\n\n"

        codigoTemp += "// FUN  \n" + "\n\n".join(self.funciones_predef) + "\n\n"

        codigoTemp += "void main(){\n" + "\n".join(self.codigo) + "\n\n\t return;\n}\n"

        return codigoTemp

    # ! Genera un nuevo temporal
    def nuevoTemp(self):
        temp = "tmp" + str(self.temporal)
        self.temporal += 1
        self.tempLista.append(temp)
        return temp

    # ! Genera un nuevo label
    def nuevoLabel(self):
        temp = self.label
        self.label += 1
        return "L" + str(temp)


