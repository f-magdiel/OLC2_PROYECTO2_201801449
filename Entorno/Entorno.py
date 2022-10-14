class Entorno:
    def __init__(self, padre, flag_bucle):
        self.padre = padre
        self.flag_bucle = flag_bucle
        self.variables = {}
        self.size = 0

    def nueva_variable(self, variable):
        variable.posicion = self.size
        self.size += 1
        self.variables[variable.id] = variable


    def existe_variable(self, id):
        env = self
        while env:
            if id in env.variables:
                return True
            env = env.padre
        return False

    def obtener_variable(self, id):
        depth = 0
        env = self
        while env:
            if id in env.variables:
                return env.variables.get(id), depth
            else:
                env = env.padre
                depth += env.size
