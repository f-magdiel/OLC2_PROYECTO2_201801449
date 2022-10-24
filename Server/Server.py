import json
import random
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from Analizador.Sintactico import parser
from General.General import Salidas, List_Errores, Tabla_Simbolo, Env_General, Errores
from Entorno.Entorno import Entorno
from Enum.TipoError import TIPO_ERROR
from Enum.TipoPrimitivo import TipoPrimitivo
from Generador.Generador import Generador

lista_variables = []
lista_funciones = []
lista_errores = []

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


@app.route('/')
def index():
    return "Server online"


@app.route('/interpretar', methods=['post'])
def interpretar():
    if request.method == 'POST':
        entradas = request.json["code"]
        str_entradas = str(entradas)
        instruc = parser.parse(str_entradas)
        salida = ""
        if instruc:
            generador = Generador()
            env = Entorno(None, None)
            Env_General.append(env)
            for inst in instruc:
                inst.convertir(generador, env)
            codigo = generador.obtenerCodigo()
            salida = codigo
        else:
            alert = "Error al ejecutar instrucciones del analizador"
            List_Errores.append(Errores(0, alert, TIPO_ERROR.SEMANTICO))
        # ? TABLA SIMBOLOS
        for entorno in Env_General:
            for i in entorno.variables:

                tipo = ""
                if entorno.variables[i].tipo[0] in [TipoPrimitivo.ARREGLO, TipoPrimitivo.VECTOR]:
                    tipo = "ARREGLO"
                else:
                    tipo = "VARIABLE"
                if entorno.variables[i].tipo[0]:
                    lista = [str(entorno.variables[i].id), tipo, str(entorno.variables[i].tipo[0].value), "LOCAL", str(entorno.variables[i].fila), random.randint(0, 100)]
                    lista_variables.append(lista)
                else:
                    lista = [str(entorno.variables[i].id), tipo, str("----"), "LOCAL", str(entorno.variables[i].fila), random.randint(0, 100)]
                    lista_variables.append(lista)

            for j in entorno.funciones:
                lista = [str(entorno.funciones[j].id), "FUNCION", str("VOID"), "GLOBAL", str(entorno.funciones[j].fila), random.randint(0, 100)]
                lista_variables.append(lista)

        # * Para errores

        if len(List_Errores) > 0:
            for err in List_Errores:
                _errores = [str(err.fila), random.randint(0, 100), "LOCAL O GLOBAL", str(err.tipo.name), str(err.info), str(err.tiempo)]
                lista_errores.append(_errores)
        else:
            _errores = ["", "", "", "", "", ""]
            lista_errores.append(_errores)

        res = jsonify({
            'consola': salida
        })
        salida = ""
        return res


@app.route('/getTablaSimbolos', methods=['get'])
def getTablaSimbolos():
    if request.method == 'GET':
        res = jsonify({
            'simb': lista_variables
        })

        lista_variables.clear()
        return res


@app.route('/getTablaErrores', methods=['get'])
def getTablaErrores():
    if request.method == 'GET':
        res = jsonify({
            'simb': lista_errores
        })
        print("LISTA ERR,",lista_errores)
        lista_errores.clear()
        return res


if __name__ == '__main__':
    app.run(port=7000, debug=True, host='localhost')
