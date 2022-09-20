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
        codigoTemp = '''
        #include <stdio.h>
        #include <math.h>
        double HEAP[10000];
        double HEAP[10000];
        double P;
        double H;
        '''

        if len(self.tempLista) > 0:
            codigoTemp += "double " + self.obtenerUsadoTemp() + ";\n\n"

        codigoTemp += "void main(){"
        codigoTemp += "\n".join(self.codigo)
        codigoTemp += "\n        return;\n        }\n"

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

    def agregarExpresion(self,target, ):


gen = Generador()
for i in range(100):
    t = gen.nuevoTemp()
print(gen.obtenerCodigo())
