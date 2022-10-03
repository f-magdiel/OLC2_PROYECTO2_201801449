import ply.lex as lex
from Reporte.TipoError import TIPIN_ERROR
from Reporte.Contenido import Tabla_Errorres, Errores

reservadas = {
    'i64': 'I64',
    'f64': 'F64',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'char': 'CHAR',
    'str': 'STR',
    'String': 'STRING',
    'mut': 'MUT',
    'let': 'LET',
    'fn': 'FN',
    'main': 'MAIN',
    'println': 'PRINTLN',
    'to_string': 'TOSTRING',
    'to_owned': 'TOOWNED',
    'as': 'AS',
    'pow': 'POW',
    'powf': 'POWF',
    'if': 'IF',
    'else': 'ELSE',
    'match': 'MATCH',
    'loop': 'LOOP',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'usize': 'USIZE',
    'for': 'FOR',
    'in': 'IN',
    'vec': 'VEC',
    'Vec': 'VVEC',
    'new': 'NEW',
    'with_capacity': 'WITH_CAPACITY',
    'len': 'LEN',
    'capacity': 'CAPACITY',
    'contains': 'CONTAINS',
    'remove': 'REMOVE',
    'insert': 'INSERT',
    'push': 'PUSH',
    'abs': 'ABS',
    'sqrt': 'SQRT',
    'clone': 'CLONE',
}

tokens = [

    'ID',
    'DECIMAL',
    'ENTERO',
    'CARACTER',
    'CADENA',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'IGUALQUE',
    'NOIGUALQUE',
    'MAYORIQUE',
    'MENORIQUE',
    'MAYORQUE',
    'MENORQUE',
    'OR',
    'AND',
    'NOT',
    'BARRAS',
    'SIGNOI',
    'IGUAL',
    'GUIONB',
    'PTO',
    'COMA',
    'PTCOMA',
    'DDOSPT',
    'DOSPT',
    'LLAVEIZQ',
    'LLAVEDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',

]
tokens += list(reservadas.values())

# tokens
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_MODULO = r'%'
t_IGUALQUE = r'=='
t_NOIGUALQUE = r'!='
t_MAYORIQUE = r'>='
t_MENORIQUE = r'<='
t_MAYORQUE = r'>'
t_MENORQUE = r'<'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_BARRAS = r'\|'
t_SIGNOI = r'&'
t_IGUAL = r'='
t_GUIONB = r'_'
t_PTO = r'\.'
t_COMA = r','
t_PTCOMA = r';'
t_DDOSPT = r'::'
t_DOSPT = r':'
t_LLAVEIZQ = r'{'
t_LLAVEDER = r'}'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_ENTERO = r'\d+'
t_DECIMAL = r'\d+\.\d+'

# ?---------------FUNCIONES----------------------------
def t_ID(t):
    r'([a-zA-Z]|_[a-zA-Z])[a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t


# def t_DECIMAL(t):
#     r'\d+\.\d+'
#     try:
#         t.value = float(t.value)
#     except ValueError:
#         desc = f'Valor decimal incorrecto {t.value}'
#         t.value = 0
#     return t


# def t_ENTERO(t):
#     r'\d+'
#     try:
#         t.value = int(t.value)
#     except ValueError:
#         desc = f'Valor entero incorrecto {t.value}'
#         t.value = 0
#     return t


def t_CARACTER(t):
    r'\'([^\"\n\r\\]|\\n|\\r|\\t|\\"|\\\'|\\\\)?\''
    t.value = t.value[1:-1]  # remuevo las comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\N', '\n')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\R', '\r')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\T', '\t')
    t.value = t.value.replace('\\\"', '\"')
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\\', '\\')
    return t


def t_CADENA(t):
    r'"([^\"\n\r\\]|\\n|\\r|\\t|\\"|\\\'|\\\\)*?"'
    t.value = t.value[1:-1]  # remuevo las comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\N', '\n')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\R', '\r')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\T', '\t')
    t.value = t.value.replace('\\\"', '\"')
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\\', '\\')
    return t


def t_COMENTARIO_SIMPLE(t):
    r'//[^\*].*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = ' \t\r'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    alert = 'Caracter invalido %s' % t.value[0]
    Tabla_Errorres.append((Errores(t.lexer.lineno, alert, TIPIN_ERROR.LEXICO)))
    t.lexer.skip(1)


# def __init__(self, fila, info, tipo):

# ?Construyendo el analizador léxico
lexer = lex.lex()