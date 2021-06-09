#Importar Librerias Instaladas
#pip install flask
#pip install flask-sqlalchemy   -----Para Conectar a una BD SQL
#pip install flack-marshmallow  -----Definir Esquema con la BD
#pip install marshmallow-sqlalchemy
#pip install pymysql 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Instancia de FLASK mi aplicacion
app = Flask(__name__)
#Dando la configuracion a app Cadena de Conexion
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
#Configuracion por defecto para no alertar o warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#SQL alchemy pasar la configuracion
db = SQLAlchemy(app)
#Instanciar Marshmellow utiliza la instacion de app (Marshemellow sirve para esquema)
ma = Marshmallow(app)

class Task(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  title= db.Column(db.String(70), unique=True)
  description = db.Column(db.String(100))
  #Constructor cada vez que se instancia la clase
    #Al recibir asignar los datos
  def __init__(self, title, description):
    self.title = title
    self.description = description
    #Modelo de Datos completado
#Crea las tablas
db.create_all()

class TaskSchema(ma.Schema):
  class Meta:
    fields =('id', 'title', 'description')
#Una sola Respuesta
task_schema=TaskSchema()
#Cuando sean muchas respuestas
tasks_schema=TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
  title = request.json['title']
  description = request.json['description']
  new_task = Task(title,description)
  db.session.add(new_task)
  db.session.commit()
  # print(request.json)
  # return 'recibido'
  return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
  all_tasks = Task.query.all()
  result = tasks_schema.dump(all_tasks)
  return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
  task = Task.query.get(id)

  title = request.json['title']
  description = request.json['description']

  task.title = title
  task.description = description

  db.session.commit()

  return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  task = Task.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return task_schema.jsonify(task)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})


if __name__== "__main__":
    app.run(debug=True)