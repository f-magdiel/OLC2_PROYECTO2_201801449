from enum import Enum


class TipoPrimitivo(Enum):
    I64 = 'I64'
    F64 = 'F64'
    BOOL = 'BOOL'
    CHAR = 'CHAR'
    STRING = 'STRING'
    STR = 'STR'
    NULO = 'NULO'
    TOS = 'TOS'  # ? Esto es para to_string y el to_ownewd
    TOW = 'TOW'
    ARREGLO = 'ARREGLO'
    VECTOR = 'VECTOR'
    USIZE = 'USIZE'
