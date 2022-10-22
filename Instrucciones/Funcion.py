from Abstracta.Instruccion import Instruccion
from Enum.TipoPrimitivo import TipoPrimitivo
from Enum.Nativas import NATIVAS
from Entorno.Entorno import Entorno
from Entorno.Valor import Valor
from Entorno.Variable import Variable
from Entorno.Funcion import Funcion as SymbFun
from iteration_utilities import duplicates, unique_everseen
from Tipo.ArrayTipo import ArrayTipo
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from General.General import Env_General


class Parametro():
    def __init__(self, fila, id, tipo):
        self.fila = fila
        self.id = id
        self.tipo = tipo


class Funcion(Instruccion):
    def __init__(self, fila, id, parametros, tipo, instrucciones):
        super().__init__(fila)
        self.id = id
        self.parametros = parametros
        self.tipo = tipo
        self.instrucciones = instrucciones

    def convertir(self, generador, entorno):
        # ! Validar que el id no exista en la tabla de funciones del entorno local
        if not entorno.existe_fun(self.id, True):
            # ! Obtener los id's de los parámetros
            parametros_list = []
            for param in self.parametros:
                parametros_list.append(param.id)
            # ! Validar el id de los parámetros (no repetidos)
            if not list(unique_everseen(duplicates(parametros_list))):
                # ! Crear el entorno de la función
                env_funcion = Entorno(entorno)
                Env_General.append(env_funcion)
                # ! Verificar si el tipo de la función es array
                if isinstance(self.tipo, ArrayTipo):
                    # ! Ajustar el tipo
                    self.tipo = self.tipo.obtener_tipo()
                else:
                    self.tipo = [self.tipo]

                # ! Crear variable return
                variable_return = Variable(-1, 'return', True, self.tipo)
                env_funcion.nueva_variable(variable_return)
                # ! Recorrer los parámetros para declarar las variables
                for i in range(len(self.parametros)):
                    flag_reference = False
                    # ! Verificar si el tipo es array
                    if isinstance(self.parametros[i].tipo, ArrayTipo):
                        # ! Ajustar el tipo
                        self.parametros[i].tipo = self.parametros[i].tipo.obtener_tipo()
                        flag_reference = True

                    # ! Crear la variable

                    var = Variable(self.parametros[i].fila, self.parametros[i].id, True, self.parametros[i].tipo, flag_reference)
                    env_funcion.nueva_variable(var)

                # ! Guardar la función en la tabla de funciones
                func = SymbFun(self.fila, self.id, self.parametros, self.tipo, env_funcion)
                entorno.agregar_fun(func)

                # ! Crear código de las instrucciones y temporal
                tmp1 = generador.nuevoTemp()
                codigo = f"\t// Auxiliar para restaurar ámbito\n" \
                         f"\t{tmp1} = S;\n\n"
                # ! Recorrer las instrucciones
                for instruccion in self.instrucciones:

                    # ! Validar si la instrucción es aceptada en el entorno
                    if isinstance(instruccion, Break) and env_funcion.flag_bucle:
                        print("El ambito de la funcion no acepta la instruccion.")
                    elif isinstance(instruccion, Continue) and env_funcion.flag_bucle:
                        print("El ambito de la funcion no acepta la instruccion.")
                    else:
                        # ! Traducir la instrucción y obtener el código generado
                        codigo += instruccion.convertir(generador, env_funcion) + "\n"

                # ! Generar código de la función
                codigo = f"void {self.id}() {{\n" + codigo

                # ! Validar codigo de la funicon
                if codigo.count("ETIQUETA_RETURN") > 0:
                    lbl1 = generador.nuevoLabel()
                    codigo = codigo.replace("TEMPORAL_RETURN", tmp1)
                    codigo = codigo.replace("ETIQUETA_RETURN", lbl1)

                    codigo += f"\t{lbl1}:\n"

                codigo += f"\treturn;\n" \
                          f"}}"
                generador.funciones_predef.append(codigo)

            else:
                print("Identificador duplicado en la lista deparametros.")

        else:
            print("Funcion '{}' ya declarada en el ambito.".format(self.id))
