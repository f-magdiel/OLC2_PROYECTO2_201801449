class Entorno:
    def __init__(self, padre, flag_bucle=False):
        self.padre = padre
        self.flag_bucle = flag_bucle
        self.variables = {}
        self.funciones = {}
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


# ! -------------------------FUNCIONES--------------------------------------
def agregar_fun(self, funcion):
    self.funciones[funcion.id] = funcion


def existe_fun(self, id, local):
    if local:
        return id in self.funciones
    else:
        entorno = self
        while entorno:
            if id in self.funciones:
                return True
            else:
                entorno = entorno.padre
        return False


def obtener_fun(self, id):
    entorno = self
    while entorno:
        if id in self.funciones:
            return entorno.funciones.get(id)
        else:
            entorno = entorno.padre
