from Entorno.Simbolo import Simbolo


class Entorno:
    def __init__(self, padre):
        self.padre = padre
        self.variable = {}
        self.size = 0

        if (padre != None):
            self.size = padre.size

    def guardarVariable(self, id):
        if (self.variable.get(id) != None):
            print("La variable " + id + " ya existe")

        tempVariable = Simbolo(id, self.size)
        self.size = self.size + 1
        self.variable[id] = tempVariable
        return tempVariable

    def obtenerVariable(self, id):
        tempEntorno = self
        while (tempEntorno != None):
            if (tempEntorno.variable.get(id) != None):
                return tempEntorno.variable.get(id)
            tempEntorno = tempEntorno.padre
        print("Error: La variable" + id + " no existe")
        return None
