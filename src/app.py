"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#desde Aqui el codigo
#obtener todos los user Ok = 200

@app.route("/users", methods=["GET"])
def user_list():    
    users= User.query.all()
    all_users=list(map(lambda x: x.serialize(), users)) #cogemos el sql y lo pasamos a python
    return jsonify(all_users), 200 # pasamos de python a json


#PERSONAJES

#obtengo todos los personajes 
@app.route("/personajes", methods=["GET"])
def personajes_list():
    personajes= Personajes.query.all()
    all_personajes=list(map(lambda x: x.serialize(), personajes))
    return jsonify(all_personajes), 200

#obtengo UN personaje
@app.route("/personajes/<int:id>", methods=["GET"])
def personaje_list(id):
    personaje = Personajes.query.get(id)
    return jsonify(personaje), 200


#Agregar UN personaje
@app.route("/favorite/people/<int:personaje_id>", methods=["POST"])
def agregar_personaje(personaje_id):
    user_id = request.json.get("user_id")  # es la respuesta en formato json
    favorito = Favoritos(user_id=user_id, personaje_id=personaje_id)
    
    db.session.add(favorito)
    db.session.commit()
    
    return jsonify({"msg": "Personaje agregado a favoritos"}), 201


#Borrar un personaje de favoritos
@app.route('/favorite/people/<int:personaje_id>', methods=['DELETE'])
def borrar_favorito(personaje_id):
    favorito = Favoritos.query.filter_by(personaje_id=personaje_id).first()
    
    if not favorito:
        return jsonify({"msg": "Personaje no encontrado en favoritos"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify({"msg": "Favorito eliminado"}), 200



#PLANETAS

#obtengo todos los planetas
@app.route("/planetas", methods=["GET"])
def planetas_list():
    planetas= Planetas.query.all()
    all_planetas=list(map(lambda x: x.serialize(), planetas))
    return jsonify(all_planetas), 200

#obtengo UN planeta
@app.route("/planeta/<int:id>", methods=["GET"])
def planeta_list(id):
    planeta = Planetas.query.get(id)
    return jsonify(planeta), 200

#Agregar UN planeta
@app.route("/favorite/planet/<int:planeta_id>", methods=["POST"])
def agregar_planeta(planeta_id):
    user_id = request.json.get("user_id")
    favorito = Favoritos(user_id=user_id, planeta_id=planeta_id)
    
    db.session.add(favorito)
    db.session.commit()
    
    return jsonify({"msg": "Planeta agregado a favoritos"}), 200



#borrar planeta de favoritos
@app.route('/favorite/planeta/<int:planeta_id>', methods=['DELETE'])
def borrar_planeta_favorito(planeta_id):
    favorito = Favoritos.query.filter_by(planeta_id=planeta_id).first()
    
    if not favorito:
        return jsonify({"msg": "Planeta no encontrado en favoritos"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify({"msg": "Favorito eliminado"}), 200


#FAVORITOS

#obtengo todos los favoritos
@app.route("/favoritos", methods=["GET"])
def favoritos_list():
    favoritos= Favoritos.query.all()
    all_favoritos=list(map(lambda x: x.serialize(), favoritos))
    return jsonify(all_favoritos), 200



@app.route('/favoritos/<int:user_id>', methods=["GET"])
def obtener_favoritos(user_id):

    favoritos = Favoritos.query.filter_by(user_id=user_id).all()
    
    if not favoritos:
        return jsonify({"error": "No hay favoritos para este usuario"}), 404

    # favoritos_serializados = [favorito.serialize() for favorito in favoritos]

    favoritos_serializados=[]
    for favorito in favoritos:
        favoritos_serializados.append(favorito.serialize())

    return jsonify(favoritos_serializados), 200




# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
