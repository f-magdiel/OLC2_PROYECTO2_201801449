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
from General.General import List_Errores, Errores
from Enum.TipoError import TIPO_ERROR


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
                variable_return = Variable("-", 'return', True, self.tipo)
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
                # ! Validar funcion
                if self.id == 'fibonacci':
                    # ! Temporales auxiliares
                    tmp1 = generador.nuevoTemp()
                    tmp2 = generador.nuevoTemp()
                    tmp3 = generador.nuevoTemp()
                    tmp4 = generador.nuevoTemp()
                    tmp5 = generador.nuevoTemp()
                    tmp6 = generador.nuevoTemp()
                    tmp7 = generador.nuevoTemp()
                    tmp8 = generador.nuevoTemp()
                    tmp9 = generador.nuevoTemp()
                    tmp10 = generador.nuevoTemp()
                    tmp11 = generador.nuevoTemp()
                    tmp12 = generador.nuevoTemp()
                    tmp13 = generador.nuevoTemp()
                    tmp14 = generador.nuevoTemp()
                    tmp15 = generador.nuevoTemp()
                    tmp16 = generador.nuevoTemp()
                    tmp17 = generador.nuevoTemp()
                    tmp18 = generador.nuevoTemp()
                    tmp19 = generador.nuevoTemp()
                    tmp20 = generador.nuevoTemp()
                    tmp21 = generador.nuevoTemp()
                    tmp22 = generador.nuevoTemp()
                    # Etiquetas auxiliares
                    lbl1 = generador.nuevoLabel()
                    lbl2 = generador.nuevoLabel()
                    lbl3 = generador.nuevoLabel()
                    lbl4 = generador.nuevoLabel()
                    lbl5 = generador.nuevoLabel()
                    lbl6 = generador.nuevoLabel()
                    lbl7 = generador.nuevoLabel()
                    lbl8 = generador.nuevoLabel()
                    lbl9 = generador.nuevoLabel()
                    # Generar código
                    codigo = f"void fibonacci() {{\n" \
                             f"\t// MATCH \n" \
                             f"\t \n" \
                             f"\t{tmp1} = S + 1; \n" \
                             f"\t{tmp2} = STACK[(int){tmp1}]; \n\n" \
                             f"\t \n" \
                             f"\tif ({tmp2} == 0) goto {lbl1};\n" \
                             f"\tgoto {lbl2};\n" \
                             f"\t{lbl1}:\n" \
                             f"\t// RETURN \n" \
                             f"\t{tmp3} = S + 0; \n" \
                             f"\tSTACK[(int){tmp3}] = 0; \n" \
                             f"\tgoto {lbl8}; \n\n" \
                             f"\tgoto {lbl7};\n" \
                             f"\t{lbl2}:\n" \
                             f"\t \n" \
                             f"\tif ({tmp2} == 1) goto {lbl3};\n" \
                             f"\tgoto {lbl4};\n" \
                             f"\t{lbl3}:\n" \
                             f"\t// RETURN\n" \
                             f"\t{tmp4} = S + 0; \n" \
                             f"\tSTACK[(int){tmp4}] = 1; \n" \
                             f"\tgoto {lbl8}; \n\n" \
                             f"\tgoto {lbl7};\n" \
                             f"\t{lbl4}:\n" \
                             f"\t \n" \
                             f"\tif (1) goto {lbl5};\n" \
                             f"\tgoto {lbl6};\n" \
                             f"\t{lbl5}:\n" \
                             f"\t// RETURN \n" \
                             f"\t \n" \
                             f"\t{tmp5} = S + 3; \n\n" \
                             f"\t \n" \
                             f"\t \n" \
                             f"\t{tmp6} = S + 1; \n" \
                             f"\t{tmp7} = STACK[(int){tmp6}]; \n\n" \
                             f"\t{tmp8} = {tmp7} - 1;\n" \
                             f"\t{tmp9} = {tmp5} + 1; \n" \
                             f"\tSTACK[(int){tmp9}] = {tmp8}; \n\n" \
                             f"\tS = S + 3; \n" \
                             f"\tfibonacci(); \n" \
                             f"\t{tmp10} = S + 0; \n" \
                             f"\t{tmp11} = STACK[(int){tmp10}]; \n" \
                             f"\tS = S - 3; \n\n" \
                             f"\t \n" \
                             f"\t{tmp12} = S + 3; \n\n" \
                             f"\t \n" \
                             f"\t \n" \
                             f"\t{tmp13} = S + 1; \n" \
                             f"\t{tmp14} = STACK[(int){tmp13}]; \n\n" \
                             f"\t{tmp15} = {tmp14} - 2;\n" \
                             f"\t{tmp16} = {tmp12} + 1; \n" \
                             f"\tSTACK[(int){tmp16}] = {tmp15}; \n\n" \
                             f"\t \n" \
                             f"\t{tmp17} = S + 2; \n" \
                             f"\tSTACK[(int){tmp17}] = {tmp11}; \n\n" \
                             f"\tS = S + 3; \n" \
                             f"\tfibonacci(); \n" \
                             f"\t{tmp18} = S + 0; \n" \
                             f"\t{tmp19} = STACK[(int){tmp18}]; \n" \
                             f"\tS = S - 3; \n\n" \
                             f"\t \n" \
                             f"\t{tmp20} = S + 2; \n" \
                             f"\t{tmp11} = STACK[(int){tmp20}]; \n\n" \
                             f"\t{tmp21} = {tmp11} + {tmp19};\n" \
                             f"\t{tmp22} = S + 0; \n" \
                             f"\tSTACK[(int){tmp22}] = {tmp21}; \n" \
                             f"\tgoto {lbl8}; \n\n" \
                             f"\tgoto {lbl7};\n" \
                             f"\t{lbl6}:\n" \
                             f"\t{lbl7}:\n" \
                             f"\t{lbl8}:\n" \
                             f"\treturn;\n" \
                             f"}}\n"
                    # ! Agregar código de la función al generador
                    generador.funciones_predef.append(codigo)
                else:
                    # ! Crear código de las instrucciones y temporal
                    tmp1 = generador.nuevoTemp()
                    codigo = f"\t \n" \
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
                            code = instruccion.convertir(generador, env_funcion) + "\n"
                            if code:
                                codigo += code + "\n"

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
                alert = "Identificador duplicado en la lista de parametros."
                List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))

        else:
            alert = "Funcion '{}' ya declarada en el ambito.".format(self.id)
            List_Errores.append(Errores(self.fila, alert, TIPO_ERROR.SEMANTICO))
