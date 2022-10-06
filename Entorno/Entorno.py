class Entorno:
    def __init__(self, padre, flag_bucle):
        self.padre = padre
        self.flag_bucle = flag_bucle
        self.variables = {}
        self.size = 0

    def nueva_variable(self, var):
        var.posicion = self.size
        self.size += 1
        self.variables[id] = var

    def existe_variable(self, id):
        ent = self
        while ent:
            if id in ent.variables:
                return True
            ent = ent.padre
        return False

    def obtener_variable(self, id):
        ent = self
        while ent:
            if id in ent.variables:
                return ent.variables.get(id)
            else:
                ent = ent.padre
