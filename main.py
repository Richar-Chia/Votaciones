from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import pymongo
import certifi
from Controladores.ControladorMesa import ControladorMesa
from Controladores.ControladorPartido import  ControladorPartido
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.ControladorResultado import ControladorResultado

app = Flask(__name__)
cors = CORS(app)
miControladorMesa = ControladorMesa()
miControladorPartido = ControladorPartido()
miControladorCandidato = ControladorCandidato()
miControladorResultado = ControladorResultado()

ca = certifi.where()
client = pymongo.MongoClient("mongodb+srv://rinwer:824657919@cluster0.g0rlmpl.mongodb.net/DataBaseUniversidad?retryWrites=true&w=majority",tlsCAFile=ca)
db = client.test

#*************** Metodo para mostrar la info del servidor en linea. ***************#
@app.route("/", methods=['GET'])
def loadFileConfig():
    with open('config.json') as file:
        data = json.load(file)
        return data

#*************** Metodos para actualizar la coleccion Mesa ***************#
@app.route("/mesas", methods=['GET'])
def getEstudiantes():
    json = miControladorMesa.index();
    return jsonify(json);

@app.route("/mesas", methods=['POST'])
def crearEstudiante():
    data = request.get_json();
    print("hola: ", data)
    json = miControladorMesa.create(data)
    return jsonify(json)

@app.route("/mesas/<string:id>", methods=['GET'])
def getEstudiante(id):
    json = miControladorMesa.show(id);
    return jsonify(json)

@app.route("/mesas/<string:id>", methods=['PUT'])
def modificarEstudiante(id):
    data = request.get_json();
    json = miControladorMesa.update(id, data);
    return jsonify(json);

@app.route("/mesas/<string:id>", methods=['DELETE'])
def eliminarEstudiante(id):
    json = miControladorMesa.delete(id);
    return jsonify(json);

#*************** Metodos para coleccion partidos ***************#
@app.route("/partidos", methods=['GET'])
def getPartidos():
    json = miControladorPartido.index();
    return jsonify(json);

@app.route("/partidos", methods=['POST'])
def crearPartido():
    data = request.get_json();
    print("hola: ", data)
    json = miControladorPartido.create(data)
    return jsonify(json)

@app.route("/partidos/<string:id>", methods=['GET'])
def getPartido(id):
    json = miControladorPartido.show(id);
    return jsonify(json)

@app.route("/partidos/<string:id>", methods=['PUT'])
def modificarPartido(id):
    data = request.get_json();
    json = miControladorPartido.update(id, data);
    return jsonify(json);

@app.route("/partidos/<string:id>", methods=['DELETE'])
def eliminarPartido(id):
    json = miControladorPartido.delete(id);
    return jsonify(json);

#*************** Metodos para coleccion candidatos ***************#
@app.route("/candidatos", methods=['GET'])
def getcandidatos():
    json = miControladorCandidato.index();
    return jsonify(json);

@app.route("/candidatos", methods=['POST'])
def crearcandidato():
    data = request.get_json();
    print("hola: ", data)
    json = miControladorCandidato.create(data)
    return jsonify(json)

@app.route("/candidatos/<string:id>", methods=['GET'])
def getcandidato(id):
    json = miControladorCandidato.show(id);
    return jsonify(json)

@app.route("/candidatos/<string:id>", methods=['PUT'])
def modificarcandidato(id):
    data = request.get_json();
    json = miControladorCandidato.update(id, data);
    return jsonify(json);

@app.route("/candidatos/<string:id>", methods=['DELETE'])
def eliminarcandidato(id):
    json = miControladorCandidato.delete(id);
    return jsonify(json);

#*************** 1-n relación Partido-candidatos ***************#
@app.route("/candidatos/<string:id>/partidos/<string:id_partido>",methods=['PUT'])
def asignarPartidoACandidato(id,id_partido):
    json=miControladorCandidato.asignarPartido(id,id_partido)
    return jsonify(json)

#*************** relació n-n colección resultados ***************#

#-------listar todos los resultados de todas las mesas-------#
@app.route("/resultados",methods=['GET'])
def getResultadoes():
    json=miControladorResultado.index()
    return jsonify(json)

#-------Resultados por id-------#
@app.route("/resultados/<string:id>",methods=['GET'])
def getResultado(id):
    json=miControladorResultado.show(id)
    return jsonify(json)

#-------Ingresar votos por mesa y candidato-------#
@app.route("/resultados/mesa/<string:id_mesa>/candidato/<string:id_candidato>",methods=['POST'])
def crearResultado(id_mesa,id_candidato):
    data = request.get_json()
    json=miControladorResultado.create(data,id_mesa,id_candidato)
    return jsonify(json)

#-------Actualizar votos de un documento existente por id mesa y id candidato-------#
@app.route("/resultados/<string:id_resultado>/mesa/<string:id_mesa>/candidato/<string:id_candidato>",methods=['PUT'])
def modificarResultado(id_resultado,id_mesa,id_candidato):
    data = request.get_json()
    json=miControladorResultado.update(id_resultado,data,id_mesa,id_candidato)
    return jsonify(json)

#-------Eliminar documento votos por id.-------#
@app.route("/resultados/<string:id_resultado>",methods=['DELETE'])
def eliminarResultado(id_resultado):
    json=miControladorResultado.delete(id_resultado)
    return jsonify(json)

#-------Votos por candidato en todas las mesas-------#
@app.route("/resultados/candidato/<string:id_candidato>",methods=['GET'])
def votosPorCandidato(id_candidato):
    json=miControladorResultado.listarVotosPorCandidato(id_candidato)
    return jsonify(json)

#-------Cantidado con votos mas altos-------#
@app.route("/resultados/votos_mayores",methods=['GET'])
def getVotosMayores():
    json=miControladorResultado.votosMasAltosPorCandidato()
    return jsonify(json)

#-------Promedio votos por canditado en todas las mesas-------#
@app.route("/resultados/promedio_votos/candidato/<string:id_candidato>",methods=['GET'])
def getPromedioVotosPorCandidato(id_candidato):
    json=miControladorResultado.promedioVotosPorCandidato(id_candidato)
    return jsonify(json)


if __name__ == '__main__':

    dataConfig = loadFileConfig()
    baseDatos = client["votaciones"];
    #print(baseDatos.list_collection_names());
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])