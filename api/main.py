import json
from flask import Flask,jsonify
from sqlalchemy import create_engine
from faker import Faker
app = Flask(__name__)

connection_db = "postgresql://postgres_user:postgrespwd@db:5432/postgresdb"
app.config["SQLACHEMY_DATABASE_URI"] = connection_db
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(connection_db)

@app.route('/listausuarios', methods=["POST"])
def mostrar():
    personas = []
    try:
        request = engine.execute("SELECT nombre, telefono FROM usuarios")
        personas = request.fetchall()
        json_string = json.dumps(personas, default=str)
    except:
        return jsonify({"Respuesta":"Los Datos no se han podido obtener correctamente"})
    return json_string

@app.route('/insertardatos', methods=["POST"])
def insertar_datos():
    fake = Faker()
    try:
        for i in range(5):
            nombre = fake.name()
            tel = fake.phone_number()
            engine.execute(f"INSERT INTO usuarios(nombre,telefono) values('{nombre}','{tel}')")
    except:
        return jsonify({"Respuesta":"Ha ocurrido un error y no se han podido insertar los datos."})
    return jsonify({"Respuesta":"Los datos se han insertado correctamente."})
    
@app.route('/creartabla', methods=["POST"])
def crear_tabla():
    try:
        engine.execute("CREATE TABLE IF NOT EXISTS usuarios(id serial, nombre varchar(200), telefono varchar(200))")
    except:
        return jsonify({"Respuesta":"He Fallado"})
    return jsonify({"Respuesta":"Se ha creado la tabla correctamente"})
if __name__=="__main__":
    app.run(host="0.0.0.0",port=80) 