class Generador:
    def __init__(self):
        self.generador = None
        self.temporal = 0
        self.label = 0
        self.codigo = []
        self.tempLista = []

    # ! Se obtiene los temporales usados
    def obtenerUsadoTemp(self):
        return ",".join(self.tempLista)

    def obtenerCodigo(self):
        codigoTemp = ""
        codigoTemp += "#include <stdio.h>\n"
        codigoTemp += "#include <math.h>\n"
        codigoTemp += "double HEAP[10000];\n"
        codigoTemp += "double STACK[10000];\n"
        codigoTemp += "double P;\n"
        codigoTemp += "double H;\n"



        if len(self.tempLista) > 0:
            codigoTemp += "double " + self.obtenerUsadoTemp() + ";\n\n"

        codigoTemp += "void main(){\n"
        codigoTemp += "\n".join(self.codigo)
        codigoTemp += "\nreturn;\n}\n"

        return codigoTemp

    # ! Genera un nuevo temporal
    def nuevoTemp(self):
        temp = "t" + str(self.temporal)
        self.temporal = self.temporal + 1

        self.tempLista.append(temp)
        return temp

    def nuevoLabel(self):
        temp = self.label
        self.label = self.label + 1
        return "L" + str(temp)

    def agregarLlamadaFuncion(self, nombre):
        self.codigo.append(nombre + "();")

    def agregarLabel(self, label):
        self.codigo.append(label + ":")

    def agregarExpresion(self, target, left, right, operador):
        self.codigo.append(target + " = " + left + " " + operador + " " + right + ";")

    def agregarIf(self, left, right, operador, label):
        self.codigo.append("if(" + left + " " + operador + " " + right + ") goto " + label + ";")

    def agregarGoto(self, label):
        self.codigo.append("goto " + label + ";")

    def agregarPrintf(self, tipo, valor):
        self.codigo.append("printf(\"%" + tipo + "\"," + valor + ");")

    def agregarSaltoLinea(self):
        self.codigo.append("printf(\"%c\",10;")

    def sigHeap(self,):
        self.codigo.append("P = P + " + "1" + ";")

    def antHeap(self,):
        self.codigo.append("P = P - " + "1" + ";")

    def obtenerValorHeap(self, target, index):
        self.codigo.append(target + "= HEAP[(int)" + index + "];")

    def agregarValorHeap(self, index, valor):
        self.codigo.append("HEAP[(int)" + index + "] = " + valor + ";")

    def obtenerValorStack(self, target, index):
        self.codigo.append(target + " = STACK[(int)" + index + "];")

    def agregarValorStack(self, index, valor):
        self.codigo.append("STACK[(int)" + index + "] = " + valor + ";")



