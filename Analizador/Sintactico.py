import ply.yacc as yacc
from Analizador.Lexico import tokens
from Enum.TipoPrimitivo import TipoPrimitivo
from Reporte.TipoError import TIPIN_ERROR
from Reporte.Contenido import Tabla_Errorres, Errores
from Instrucciones.Imprimir import Imprimir
from Generador.Generador import Generador
from Entorno.Entorno import Entorno
from Instrucciones.Declaracion import Declaracion
from Expresiones.FuncionesNativas import FuncionNativa
from Enum.Nativas import NATIVAS
from Expresiones.Primitiva import Primitiva
from Expresiones.Aritmetica import Aritmetica
from Enum.OpAritmetico import OPERADOR_ARITMETICO
from Enum.OpUnario import OPERADOR_UNARIO
from Expresiones.Unaria import Unaria
from Expresiones.Relacional import Relacional
from Enum.OpRelacional import OPERADOR_RELACIONAL
from Expresiones.Casteo import Casteo
from Instrucciones.Main import Main
from Instrucciones.If import If
from Expresiones.Logica import Logica
from Enum.OpLogico import OPERADOR_LOGICO
from Instrucciones.While import While
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Loop import Loop
from Expresiones.Arreglos import Arreglo
from Instrucciones.Match import Match
from Expresiones.NewArreglo import NewArreglo
from Expresiones.Vectores import Vector
from Expresiones.NewVector import NewVector
from Expresiones.VectorUnico import VectorUnico
from Expresiones.VectorNativa import VectorNativa
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Forin import Forin
from Expresiones.Acceso import Acceso
from Instrucciones.NativaVector import NativaVector
from Instrucciones.Funcion import Parametro, Funcion
from Expresiones.Remove import Remove
from Tipo.ArrayTipo import ArrayTipo
from Expresiones.LLamadaFuncion import LlamadaFuncion as LLamadaFuncionExpres
from Instrucciones.Return import Return
from Instrucciones.LlamadaFuncion import LlamadaFuncion
from Expresiones.IfExpresion import IfExpresion

#
# # ?--------------------------------------------------PRECEDENCIAS-----------------------------------------------------
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALQUE', 'NOIGUALQUE', 'MENORQUE', 'MENORIQUE', 'MAYORQUE', 'MAYORIQUE'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'DIVIDIDO', 'POR', 'MODULO'),
    ('left', 'AS'),
    ('right', 'UMENOS', 'NOT'),
    ('nonassoc', 'PTO'),

)


# # ?--------------------------------------------PRODUCCIONES------------------------------------------------------------
def p_inicio_inicio(t):
    'inicio : instrucciones'
    t[0] = t[1]


#
#
# def p_inicio1(t):
#     'inicio : instrucciones main'
#     t.lexer.lineno = 1
#     t.lineno = 1
#     t[1].append(t[2])  # ?----> como una lista
#     t[0] = t[1]
#
#
# def p_inicio3(t):
#     'inicio : main instrucciones'
#     t[2].append(t[1])
#     t[0] = t[2]


#
#
# def p_inicio2(t):
#     'inicio : main'
#     t.lexer.lineno = 1
#     t.lineno = 1
#     t[0] = [t[1]]  # ? ----> como una lista
#
#


#
#


# def p_inicio(t):
#     'inicio : instrucciones'
#     generadorGlob = Generador()
#     entornoGlob = Entorno(None)
#     for instru in t[1]:
#         if instru:
#             instru.generador = generadorGlob
#             # instru.convertir(entornoGlob)
#             generadorGlob.codigo.append(instru.convertir(entornoGlob))
#
#     t[0] = generadorGlob.obtenerCodigo()
# ! ---------------------------------------INSTRUCCIONES---------------------------------------
def p_instrucciones1(t):
    'instrucciones : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones2(t):
    'instrucciones : instruccion'
    t[0] = [t[1]]


def p_instrucciones3(t):
    'instrucciones : '
    t[0] = []


#
#
def p_instrucion(t):
    '''instruccion : imprimir PTCOMA
                    | if
                    | while
                    | continue PTCOMA
                    | break PTCOMA
                    | loop
                    | match
                    | declaracion PTCOMA
                    | asignacion PTCOMA
                    | forin
                    | nativas_vector PTCOMA
                    | funciones
                    | return PTCOMA
                    | llamada_funciones PTCOMA   '''
    #
    #
    #                     | llamada_funciones PTCOMA
    #                     | declaracion_arreglos
    #                     | declaracion_vector
    #                     | nativas_vector
    #     '''
    t[0] = t[1]


#
#
# # !-------------------------------------VECTORES-----------------------------------------------------------------
# def p_declaracion_vec1(t):
#     'declaracion_vector : LET MUT ID DOSPT VVEC MENORQUE tipo MAYORQUE IGUAL expresion PTCOMA'
#     t[0] = DeclaracionVector(t.lineno(1), t[3], t[10], t[7], True)
#
#
# def p_declaracion_vec2(t):
#     'declaracion_vector : LET ID DOSPT VVEC MENORQUE tipo MAYORQUE IGUAL expresion PTCOMA'
#     t[0] = DeclaracionVector(t.lineno(1), t[2], t[9], t[6], False)
#
#
# def p_vector_inicio(t):
#     'expresion : VEC NOT CORIZQ expresiones CORDER'
#     vec = Arreglo(t.lineno(1), t[4])
#     t[0] = Vector(t.lineno(1), vec)
#
#
# def p_vector1(t):
#     'expresion : VVEC DOSPT DOSPT NEW PARIZQ PARDER'
#     t[0] = CreacionVector(t.lineno(1))
#
#
# def p_vector2(t):
#     'expresion : VVEC DOSPT DOSPT WITH_CAPACITY PARIZQ expresion PARDER'
#     t[0] = CreacionVector(t.lineno(1), t[6])
#
#
def p_expresion_vector1(t):
    'expresion : VEC NOT CORIZQ expresiones CORDER'
    t[0] = Vector(t.lineno(1), t[4])


def p_expresion_vector2(t):
    'expresion : VEC NOT CORIZQ expresion PTCOMA expresion CORDER'
    t[0] = NewVector(t.lineno(1), t[4], t[6])


def p_expresion_vector3(t):
    'expresion : VVEC DDOSPT NEW PARIZQ PARDER'
    t[0] = VectorUnico(t.lineno(1))


def p_expresion_vector4(t):
    'expresion : VVEC DDOSPT WITH_CAPACITY PARIZQ expresion PARDER'
    t[0] = VectorUnico(t.lineno(1), t[5])


# # !-------------------------------------NATIVAS VECTORES-------------------------------------------
def p_nativa_vec(t):
    'expresion : nativas_vec'
    t[0] = t[1]


# * --------------------------------LEN-------------------------------------

def p_nativa_len(t):
    'nativas_vec : expresion PTO LEN PARIZQ PARDER'
    t[0] = VectorNativa(t.lineno(1), t[1], NATIVAS.LEN)


#
#
# # * -------------------------------CAPACITY-------------------------------
def p_nativa_capacity(t):
    'nativas_vec : expresion PTO CAPACITY PARIZQ PARDER '
    t[0] = VectorNativa(t.lineno(1), t[1], NATIVAS.CAPACITY)


#
#
# # * ---------------------------------PUSH------------------------------------
def p_nativa_push(t):
    'nativas_vector : ID PTO PUSH PARIZQ expresion PARDER '
    t[0] = NativaVector(t.lineno(1), t[1], NATIVAS.PUSH, t[5], None)


#
#
# # * -------------------------------INSERT--------------------------------------
def p_nativa_insert(t):
    'nativas_vector : ID PTO INSERT PARIZQ expresion COMA expresion PARDER '
    t[0] = NativaVector(t.lineno(1), t[1], NATIVAS.INSERT, t[5], t[7])


#
#
# # * --------------------------REMOVE-------------------------------------------
def p_nativa_remove(t):
    'nativas_vector : ID PTO REMOVE PARIZQ expresion PARDER'
    t[0] = NativaVector(t.lineno(1), t[1], NATIVAS.REMOVE, t[5], None)


#
#
def p_nativa_remove_expre(t):
    'expresion : expresion PTO REMOVE PARIZQ expresion PARDER'
    t[0] = Remove(t.lineno(1), t[1].id, t[5])


#
#
# # * ---------------------------------CONTAINS----------------------------------
def p_nativa_contain(t):
    'nativas_vec : expresion PTO CONTAINS PARIZQ SIGNOI expresion PARDER'
    t[0] = VectorNativa(t.lineno(1), t[1], NATIVAS.CONTAINS, t[6])


#
#
# # !----------------------------------------------FUNCIONES---------------------------------------------------------

def p_funciones_2(t):
    'funciones : FN ID PARIZQ lparametros PARDER MENOS MAYORQUE tipos LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Funcion(t.lineno(1), t[2], t[4], t[8], t[10])


# fila, id, para, tipo, instruc
#
# def p_funciones_2(t):
#     'funciones : FN ID PARIZQ PARDER MENOS MAYORQUE tipo LLAVEIZQ instrucciones LLAVEDER'
#     t[0] = Funciones(t.lineno(1), t[7], t[2], [], t[9])
#
#
def p_funciones_1(t):
    'funciones : FN ID PARIZQ lparametros PARDER LLAVEIZQ instrucciones LLAVEDER '
    if t[2] == 'main':
        t[0] = Main(t.lineno(1), t[7])
    else:
        t[0] = Funcion(t.lineno(1), t[2], t[4], None, t[7])


#
#
# def p_funciones_4(t):
#     'funciones : FN ID PARIZQ PARDER LLAVEIZQ instrucciones LLAVEDER'
#     t[0] = Funciones(t.lineno(1), tipoPrimitivo.NULO, t[2], [], t[6])
#
#
def p_parametros(t):
    'lparametros : lparametros COMA lparame'
    t[1].append(t[3])
    t[0] = t[1]


def p_parametro_1(t):
    'lparametros : lparame'
    t[0] = [t[1]]


def p_parametro_2(t):
    'lparametros : '
    t[0] = []


def p_parametro_3(t):
    'lparame : ID DOSPT tipo_primitivo'
    t[0] = Parametro(t.lineno(1), t[1], [t[3]])


def p_parametro_4(t):
    '''lparame : ID DOSPT SIGNOI MUT tipo_arreglo
                | ID DOSPT SIGNOI MUT tipo_vector'''
    t[0] = Parametro(t.lineno(1), t[1], t[5])


#
#
# def p_parametro_4(t):
#     'lparame : ID DOSPT SIGNOI MUT VVEC MENORQUE tipo MAYORQUE'
#     t[0] = Parametros(tipoPrimitivo.VECTOR, t[1], False, [t[7]])
#
#
def p_llamada_funcion_inicio(t):
    'llamada_funciones : ID PARIZQ largumentos PARDER'
    t[0] = LlamadaFuncion(t.lineno(1), t[1], t[3])


def p_argumentos_0(t):
    'largumentos : largumentos COMA largumento'
    t[1].append(t[3])
    t[0] = t[1]


def p_argumentos_1(t):
    'largumentos : largumento'
    t[0] = [t[1]]


def p_argumentos_2(t):
    'largumentos : '
    t[0] = []


def p_argumentos_4(t):
    'largumento : SIGNOI MUT expresion'
    if isinstance(t[3], Acceso):
        t[3].flag_argumento = True

    t[0] = t[3]


def p_argumentos_5(t):
    'largumento : expresion'
    t[0] = t[1]


#
#
# def p_argumentos_4(t):
#     'largumento : SIGNOI MUT expresion'
#     li = [t[3], True]
#     t[0] = li
#

#
#
# # !----------------------------------------ARREGLOS---------------------------------------------------------------
# def p_arreglo_inicio(t):
#     'declaracion_arreglos : LET MUT ID DOSPT tipo_arreglo IGUAL expresion PTCOMA'
#     t[0] = DeclaracionArreglos(t.lineno(1), t[3], t[5], t[7], True)
#
#
# def p_arreglo_inicio2(t):
#     'declaracion_arreglos : LET ID DOSPT tipo_arreglo IGUAL expresion PTCOMA'
#     t[0] = DeclaracionArreglos(t.lineno(1), t[2], t[4], t[6], False)
#
#
# def p_arreglo_tipo(t):
#     'tipo_arreglo : CORIZQ tipo_arreglo PTCOMA expresion CORDER'
#     t[2].append(t[4])
#     t[0] = t[2]
#
#
def p_arreglo_tipo2(t):
    'tipo_arreglo : CORIZQ tipos PTCOMA expresion CORDER'
    t[0] = ArrayTipo(t[2], True)


def p_vector_tipo(t):
    ' tipo_vector : VVEC MENORQUE tipos MAYORQUE'
    t[0] = ArrayTipo(t[3])


# # !---------------------------------------------------IMPRIMIR---------------------------------------------------------
#
# def p_imprimir1(t):
#     'imprimir : PRINTLN NOT PARIZQ expresion COMA expresiones PARDER PTCOMA'
#     #tmp = [t[4], t[6]]
#     #tmp.append(t[4])
#     #tmp.append(t[6])
#     # t[4].append(t[6])
#     t[0] = Imprimir(t.lineno(2), t[6])


#
#
def p_imprimir2(t):
    'imprimir : PRINTLN NOT PARIZQ expresiones PARDER'
    t[0] = Imprimir(t.lineno(2), t[4])


#
#
# # !--------------------------------------------DECLARACION-------------------------------------------------------------
#
def p_declaracion1(t):
    'declaracion : LET MUT ID DOSPT tipos IGUAL expresion '
    t[0] = Declaracion(t.lineno(1), t[5], str(t[3]), t[7], True)


#
#
def p_declaracion2(t):
    'declaracion : LET MUT ID IGUAL expresion'
    t[0] = Declaracion(t.lineno(1), TipoPrimitivo.NULO, str(t[3]), t[5], True)


#
#
def p_declaracion3(t):
    'declaracion : LET ID DOSPT tipos IGUAL expresion '
    t[0] = Declaracion(t.lineno(1), t[4], str(t[2]), t[6], False)


def p_declaracion4(t):
    'declaracion : LET ID IGUAL expresion '
    t[0] = Declaracion(t.lineno(2), TipoPrimitivo.NULO, str(t[2]), t[4], False)


# # !-----------------------------------------------ASIGNACION----------------------------------------------------------
def p_asignacion1(t):
    'asignacion : ID IGUAL expresion'
    t[0] = Asignacion(t.lineno(1), t[1], t[3])


def p_asignacion2(t):
    'asignacion : ID indices IGUAL expresion'
    t[0] = Asignacion(t.lineno(1), t[1], t[4], t[2])


def p_indices_1(t):
    'indices : indices indice'
    t[1].append(t[2])
    t[0] = t[1]


def p_indices_2(t):
    'indices : indice'
    t[0] = [t[1]]


def p_indice(t):
    'indice : CORIZQ expresion CORDER'
    t[0] = t[2]


# # !---------------------------------------------------IF------------------------------------------------------------
def p_if(t):
    'if : IF expresion LLAVEIZQ instrucciones LLAVEDER '
    sentencia = {'exp': t[2], 'instrs': t[4]}
    sentencias = [sentencia]  # [{exp_cond, instrucciones}]
    t[0] = If(t.lineno(1), sentencias)


def p_else_if(t):
    'if : IF expresion LLAVEIZQ instrucciones LLAVEDER else'
    sentencia = {'exp': t[2], 'instrs': t[4]}
    sentencias = [sentencia]  # [{exp_cond, instrucciones}]
    t[0] = If(t.lineno(1), sentencias, t[6])


def p_else_if_else_if(t):
    'if : IF expresion LLAVEIZQ instrucciones LLAVEDER lelseif'
    sentencia = {'exp': t[2], 'instrs': t[4]}
    sentencias = [sentencia]  # [{exp_cond, instrucciones}]
    sentencias += t[6]
    t[0] = If(t.lineno(1), sentencias)


def p_else_if_else(t):
    'if : IF expresion LLAVEIZQ instrucciones LLAVEDER lelseif else'
    sentencia = {'exp': t[2], 'instrs': t[4]}
    sentencias = [sentencia]  # [{exp_cond, instrucciones}]
    sentencias += t[6]
    t[0] = If(t.lineno(1), sentencias, t[7])


def p_else_if1(t):
    'lelseif : lelseif elseif'
    t[1].append(t[2])
    t[0] = t[1]


def p_else_if2(t):
    'lelseif : elseif'
    t[0] = [t[1]]


def p_else_if3(t):
    'elseif : ELSE IF expresion LLAVEIZQ instrucciones LLAVEDER'
    t[0] = {'exp': t[3], 'instrs': t[5]}


def p_else(t):
    'else : ELSE LLAVEIZQ instrucciones LLAVEDER'
    t[0] = t[3]


#
#
# # !-------------------------------------------MATCH---------------------------------------------------
def p_match(t):
    'match : MATCH expresion LLAVEIZQ brazos LLAVEDER'
    t[0] = Match(t.lineno(1), t[2], t[4])


def p_brazos_1(t):
    'brazos : brazos brazo'
    t[1].append(t[2])
    t[0] = t[1]


def p_brazos_2(t):
    'brazos : brazo'
    t[0] = [t[1]]


def p_brazo_1(t):
    'brazo : coincidencias IGUAL MAYORQUE LLAVEIZQ instrucciones LLAVEDER'
    t[0] = {'exps': t[1], 'instrs': t[5]}


def p_brazo_2(t):
    'brazo : coincidencias IGUAL MAYORQUE instr_match COMA'
    t[0] = {'exps': t[1], 'instrs': [t[4]]}


def p_coincidencias_1(t):
    'coincidencias : coincidencias BARRAS coincidencia'
    t[1].append(t[3])
    t[0] = t[1]


def p_coincidencias_2(t):
    'coincidencias : coincidencia'
    t[0] = [t[1]]


def p_coincidencia_1(t):
    'coincidencia : expresion'
    t[0] = t[1]


def p_coincidencia_2(t):
    'coincidencia : GUIONB'
    t[0] = t[1]


def p_instrs_match(t):
    '''instr_match : imprimir
                   | if
                   | while
                   | break
                   | continue
                   | loop
                   | match
                   | declaracion
                   | asignacion
                   | forin
                   | nativas_vector
                   | funciones
                   | return
                   | llamada_funciones '''
    t[0] = t[1]


# # * --------------------------------------------------LOOP--------------------------------------------------
# # ! -----------------------LOOP----------------------------
def p_loop_inicio(t):
    'loop : LOOP LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Loop(t.lineno(1), t[3])


#
#
# # ! -------------------WHILE-------------------------------
def p_while_inicio(t):
    'while : WHILE expresion LLAVEIZQ instrucciones LLAVEDER'
    t[0] = While(t.lineno(1), t[2], t[4])


#
#
# # ! ------------------------------FORIN--------------------------------
def p_forin_inicio(t):
    'forin : FOR ID IN expresion LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Forin(t.lineno(1), t[2], t[4], t[6])


def p_forin_2(t):
    'forin : FOR ID IN expresion PTO PTO expresion LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Forin(t.lineno(1), t[2], t[4], t[9], t[7])


#
#
# # * ---------------------------------------BREAK------------------------------------
def p_break_inicio(t):
    'break : BREAK'
    t[0] = Break(t.lineno(1))


#
#
# def p_break_expresion(t):
#     'break : BREAK expresion PTCOMA'
#     t[0] = BreakExpresion(t.lineno(1), t[2])
#
#
# # * --------------------------------------CONTINUE-------------------------------------
def p_continue_inicio(t):
    'continue : CONTINUE'
    t[0] = Continue(t.lineno(1))


#
#
# # * -------------------------------------------RETURN-----------------------------------
#
def p_instruccion_return(t):
    'return : RETURN expresion '
    t[0] = Return(t.lineno(1), t[2])


#
#
# # !----------------------------------------------------TIPO-----------------------------------------------------------
#
def p_tipo2(t):
    '''tipos : tipo_primitivo
            | tipo_arreglo
            | tipo_vector '''
    t[0] = t[1]


def p_tipo1(t):
    '''tipo_primitivo : I64
                    | F64
                    | BOOL
                    | CHAR
                    | STRING
                    | USIZE
    '''
    tipo = t[1]
    if (tipo == 'i64'):
        t[0] = TipoPrimitivo.I64
    elif (tipo == 'f64'):
        t[0] = TipoPrimitivo.F64
    elif (tipo == 'bool'):
        t[0] = TipoPrimitivo.BOOL
    elif (tipo == 'char'):
        t[0] = TipoPrimitivo.CHAR
    elif (tipo == 'String'):
        t[0] = TipoPrimitivo.STRING
    elif (tipo == 'usize'):
        t[0] = TipoPrimitivo.I64


#
#
def p_tiposino(t):
    'tipo_primitivo : SIGNOI STR'
    t[0] = TipoPrimitivo.STR


#
#
# # !------------------------------------------------EXPRESIONES---------------------------------------------------------
def p_expresiones1(t):
    ' expresiones : expresiones COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]


#
#
def p_expresiones2(t):
    'expresiones : expresion'
    t[0] = [t[1]]


def p_expresiones3(t):
    'expresiones : '
    t[0] = []


#
#
# def p_expresion_id(t):
#     'expresion : ID'
#     t[0] = Id(t.lineno(1), str(t[1]))
#
#
def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitiva(t.lineno(1), TipoPrimitivo.I64, str(t[1]))


#
#
def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitiva(t.lineno(1), TipoPrimitivo.F64, str(t[1]))


#
#
def p_expresion_true(t):
    'expresion : TRUE'
    t[0] = Primitiva(t.lineno(1), TipoPrimitivo.BOOL, "1")


def p_expresion_false(t):
    'expresion : FALSE'
    t[0] = Primitiva(t.lineno(1), TipoPrimitivo.BOOL, "0")


#
#
def p_expresion_to(t):
    '''expresion : tostring
                | toowned'''
    t[0] = t[1]


#
#
def p_expresion_tostring(t):
    'tostring : expresion PTO TOSTRING PARIZQ PARDER '
    t[0] = FuncionNativa(t.lineno(2), NATIVAS.TOSTRING, t[1])


def p_expresion_toowned(t):
    'toowned : expresion PTO TOOWNED PARIZQ PARDER '
    t[0] = FuncionNativa(t.lineno(2), NATIVAS.TOOWNED, t[1])


def p_expresion_cadena1(t):
    'expresion : CADENA'
    t[0] = Primitiva(t.lineno(1), TipoPrimitivo.STR, str(t[1]))


def p_expresion_caracter(t):
    'expresion : CARACTER'
    t[0] = Primitiva(t.lineno(1), TipoPrimitivo.CHAR, str(t[1]))


def p_expresion_aritmetica1(t):
    '''expresion : expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion POR expresion
                    | expresion DIVIDIDO expresion
                    | expresion MODULO expresion'''

    operador = t[2]

    if operador == '+':
        t[0] = Aritmetica(t.lineno(2), t[1], OPERADOR_ARITMETICO.MAS, t[3])
    elif operador == '-':
        t[0] = Aritmetica(t.lineno(2), t[1], OPERADOR_ARITMETICO.MENOS, t[3])
    elif operador == '*':
        t[0] = Aritmetica(t.lineno(2), t[1], OPERADOR_ARITMETICO.POR, t[3])
    elif operador == '/':
        t[0] = Aritmetica(t.lineno(2), t[1], OPERADOR_ARITMETICO.DIVIDIDO, t[3])
    elif operador == '%':
        t[0] = Aritmetica(t.lineno(2), t[1], OPERADOR_ARITMETICO.MODULO, t[3])


#
#
def p_exp_unaria(t):
    '''expresion : MENOS expresion %prec UMENOS
                | NOT expresion'''

    operador = str(t[1])

    if operador == '-':
        t[0] = Unaria(t.lineno(1), OPERADOR_UNARIO.MENOS, t[2])
    elif operador == '!':
        t[0] = Unaria(t.lineno(1), OPERADOR_UNARIO.NOT, t[2])


#
#
def p_expresion_aritmetica2(t):
    '''expresion : I64 DDOSPT POW PARIZQ expresion COMA expresion PARDER
                | F64 DDOSPT POWF PARIZQ expresion COMA expresion PARDER'''
    reserv = t[3]

    if reserv == 'powf':
        t[0] = Aritmetica(t.lineno(2), t[5], OPERADOR_ARITMETICO.POTENCIAF, t[7])
    elif reserv == 'pow':
        t[0] = Aritmetica(t.lineno(2), t[5], OPERADOR_ARITMETICO.POTENCIA, t[7])
    else:
        print("Error de potencia")


#
#
def p_expresion_relacional(t):
    '''expresion : expresion IGUALQUE expresion
            | expresion NOIGUALQUE expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion MENORIQUE expresion
            | expresion MAYORIQUE expresion '''
    t[0] = Relacional(t.lineno(2), t[1], t[2], t[3])


#
#
def p_expresion_logica(t):
    '''expresion : expresion OR expresion
                | expresion AND expresion
                '''
    operador = t[2]
    if operador == '&&':
        t[0] = Logica(t.lineno(2), t[1], OPERADOR_LOGICO.AND, t[3])
    elif operador == '||':
        t[0] = Logica(t.lineno(2), t[1], OPERADOR_LOGICO.OR, t[3])


#
#
def p_exp_agrupa(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]


#
#
# def p_llamada_funcion_asig(t):
#     'expresion : llamada_funciones'
#     t[0] = t[1]
#
#

# ! -----------------------------------EXPRESION ARREGLO---------------------------------
def p_expresion_arreglo1(t):
    'expresion : CORIZQ expresiones CORDER '
    t[0] = Arreglo(t.lineno(1), t[2])


def p_expresion_arreglo2(t):
    'expresion : CORIZQ expresion PTCOMA expresion CORDER'
    t[0] = NewArreglo(t.lineno(1), t[2], t[4])


#
#
# def p_expresion_Accesarreglo(t):
#     'expresion : ID lindices'
#     t[0] = Arregloacceso(t.lineno(1), t[1], t[2])
#
#
# def p_indices1(t):
#     'lindices : lindices CORIZQ expresion CORDER'
#     t[1].append(t[3])
#     t[0] = t[1]
#
#
# def p_indices2(t):
#     'lindices : CORIZQ expresion CORDER'
#     t[0] = [t[2]]
#
#
# # *----------------------------------------------- IF ASIGNACION--------------------------------------------------
#
#
def p_if_asignacion_inicio(t):
    'expresion : if_asig'
    t[0] = t[1]


def p_else_if_else_asignacion(t):
    'if_asig : IF expresion LLAVEIZQ expresion LLAVEDER elseifa elsea'
    sentencia = {'exp1': t[2], 'exp2': t[4]}
    sentencias = [sentencia]
    sentencias += t[6]
    t[0] = IfExpresion(t.lineno(1), sentencias, t[7])


def p_else_if_else_if_asignacion(t):
    'if_asig : IF expresion LLAVEIZQ expresion LLAVEDER elseifa'
    sentencia = {'exp1': t[2], 'exp2': t[4]}
    sentencias = [sentencia]
    sentencias += t[6]
    t[0] = IfExpresion(t.lineno(1), sentencias)


def p_if_else_asig(t):
    'if_asig : IF expresion LLAVEIZQ expresion LLAVEDER elsea'
    sentencia = {'exp1': t[2], 'exp2': t[4]}
    sentencias = [sentencia]
    t[0] = IfExpresion(t.lineno(1), sentencias, t[6])


def p_if_asig(t):
    'if_asig : IF expresion LLAVEIZQ expresion LLAVEDER'
    sentencia = {'exp1': t[2], 'exp2': t[4]}
    sentencias = [sentencia]
    t[0] = IfExpresion(t.lineno(1), sentencias)


def p_elseif1_asig(t):
    'elseifa : elseifa lif'
    t[1].append(t[2])
    t[0] = t[1]


def p_elseif2_asig(t):
    'elseifa : lif'
    t[0] = [t[1]]


def p_lif_asig(t):
    'lif : ELSE IF expresion LLAVEIZQ expresion LLAVEDER'
    t[0] = {'exp1': t[3], 'exp2': t[5]}


def p_else_asig(t):
    'elsea : ELSE LLAVEIZQ expresion LLAVEDER'
    t[0] = t[3]


#
#
# def p_bloque_expre_asig(t):
#     ' bloque_expresion : bloque_expresion PTCOMA expresion'
#     t[1].append(t[3])
#     t[0] = t[1]
#
#
# def p_bloque_expre2_asig(t):
#     'bloque_expresion : expresion'
#     t[0] = [t[1]]
#
#
# # *-----------------------------------MATCH ASIGNACION-------------------------------------------
# #
# def p_match_inicio_asig(t):
#     'expresion : match_asig'
#     t[0] = t[1]
#
#
# def p_match_asig(t):
#     'match_asig : MATCH expresion LLAVEIZQ imatch_asig LLAVEDER '
#     t[0] = MatchAsignacion(t.lineno(1), t[2], t[4])
#
#
# def p_imatch_asig(t):
#     'imatch_asig : opmatch_asig COMA dmatch_asig '
#     t[1].append(t[3])
#     t[0] = t[1]
#
#
# def p_dmatch_asig(t):
#     'dmatch_asig : GUIONB IGUAL MAYORQUE LLAVEIZQ bloque_expresion LLAVEDER'
#     t[0] = [[t[1]], t[5], TIPO_MATCH.MATCHDEFAULT]
#
#
# def p_dmatch_asig2(t):
#     'dmatch_asig : GUIONB IGUAL MAYORQUE expresion'
#     t[0] = [[t[1]], [t[4]], TIPO_MATCH.MATCHDEFAULT]
#
#
# def p_opmatch_asig1(t):
#     'opmatch_asig : opmatch_asig COMA cmatch_asig'
#     t[1].append(t[3])
#     t[0] = t[1]
#
#
# def p_opmatch_asig2(t):
#     'opmatch_asig : cmatch_asig'
#     t[0] = [t[1]]
#
#
# def p_cmatch_asig(t):
#     'cmatch_asig : bloque_match_asig IGUAL MAYORQUE LLAVEIZQ bloque_expresion LLAVEDER'
#     t[0] = [t[1], t[5], TIPO_MATCH.MATCHBARRAS]
#
#
# def p_cmatch_asig2(t):
#     'cmatch_asig : bloque_match_asig IGUAL MAYORQUE expresion'
#     t[0] = [t[1], [t[4]], TIPO_MATCH.MATCHBARRAS]
#
#
# def p_bloque_match_asig(t):
#     'bloque_match_asig : bloque_match_asig BARRAS expresion'
#     t[1].append(t[3])
#     t[0] = t[1]
#
#
# def p_bloque_match_asign2(t):
#     'bloque_match_asig : expresion'
#     t[0] = [t[1]]
#
#
# # !---------------------------------------------LOOP EXPRESION-----------------------------------------------
# def p_loop_expresion_inicio(t):
#     'expresion : loop_asig'
#     t[0] = t[1]
#
#
# def p_lopp_expresion(t):
#     'loop_asig : LOOP LLAVEIZQ instrucciones LLAVEDER'
#     t[0] = Loop(t.lineno(2), t[3])
#
# ! ----------------------------------LLAMADA FUNCIONES EXPRESIONES--------------------------------------------
def p_llamada_funcion_expres(t):
    'expresion : llamada_fun_expres'
    t[0] = t[1]


def p_llamada_fun_exp1(t):
    'llamada_fun_expres : ID PARIZQ largumentos PARDER'
    t[0] = LLamadaFuncionExpres(t.lineno(1), t[1], t[3])


# # !------------------------------------CASTEO---------------------------------------------------------------------
def p_casteo(t):
    'expresion : PARIZQ expresion AS tipos PARDER'
    t[0] = Casteo(t.lineno(1), t[2], t[4])


#
#
# # !----------------------------------------FUNCIONES NATIVAS--------------------------------------------------
def p_funciones_nat_inicio(t):
    'expresion : nativas_fun '
    t[0] = t[1]


def p_funciones_nat1(t):
    '''nativas_fun : expresion PTO ABS PARIZQ PARDER
                    | expresion PTO SQRT PARIZQ PARDER'''
    fun = t[3]

    if fun == 'abs':
        t[0] = FuncionNativa(t.lineno(1), NATIVAS.ABS, t[1])
    elif fun == 'sqrt':
        t[0] = FuncionNativa(t.lineno(1), NATIVAS.SQRT, t[1])


def p_funciones_nat2(t):
    'nativas_fun : expresion PTO CLONE PARIZQ PARDER'
    t[0] = FuncionNativa(t.lineno(2), NATIVAS.CLONE, t[1])


#
# ! -------------------------------------------ACCESO VARIABLE--------------------------------------------
def p_acceso_variable_1(t):
    'expresion : ID'
    t[0] = Acceso(t.lineno(1), t[1])


def p_acceso_variable_2(t):
    'expresion : ID a_indices'
    t[0] = Acceso(t.lineno(1), t[1], t[2])


def p_aindices_1(t):
    'a_indices : a_indices a_indice'
    t[1].append(t[2])
    t[0] = t[1]


def p_aindices_2(t):
    'a_indices : a_indice'
    t[0] = [t[1]]


def p_aindice(t):
    'a_indice : CORIZQ expresion CORDER'
    t[0] = t[2]


#
# # !-----------------------------------------------ERROR----------------------------------------------------------------
def p_error(t):
    if t:
        alert = "El token '{}' es inválido en está posición".format(t.value)
        error_syntaxis = Errores(t.lexer.lineno, alert, TIPIN_ERROR.SINTACITO)
        Tabla_Errorres.append(error_syntaxis)
        while True:
            car = parser.token()
            if not car or car.type in ['LLAVEDER', 'PTCOMA']:
                break
        print(alert)
        parser.restart()
    else:
        alert = "Se detecto un error al final"
        error_syntaxis = Errores(0, alert, TIPIN_ERROR.SINTACITO)
        Tabla_Errorres.append(error_syntaxis)
        print(alert)


#
#
# def report(self):
#     return self.errors
#
#
# # !---------------------------------------Se ejecuta el parser---------------------------------------------------------
parser = yacc.yacc()
entrada = r'''
fn main() {
    let a: i64 = 25 - 25;
    let b: i64 = ((((1 + 1) / 2) as i64) * 10) / a;
    println!("{}", b);

    let x: usize = 10 + 2 - (a as usize);
    let arr: [i64; 2] = [1,2];
    println!("{}", arr[x * 2 + 10 - ((a as usize) * 20)]);
}

'''
print("Inicia analizador...")
instruc = parser.parse(entrada)

if instruc:
    generador = Generador()
    env = Entorno(None, None)
    for inst in instruc:
        inst.convertir(generador, env)
    codigo = generador.obtenerCodigo()
    print(codigo)
else:
    print("Error no hay main")

print("Finaliza analizador...")
