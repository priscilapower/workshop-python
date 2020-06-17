from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SecretKey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySql2020!@localhost/workshop-python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/')
def index():
    people = Person.query.all()

    result = []
    for person in people:
        data = {}
        data['id'] = person.id
        data['name'] = person.name
        data['email'] = person.email
        result.append(data)
    return jsonify(result)


@app.route('/person', methods=['POST'])
def insert():
    name = request.json['name']
    email = request.json['email']

    person = Person(name, email)
    db.session.add(person)
    db.session.commit()

    return "Pessoa inserida com sucesso!"


@app.route('/person/<id>', methods=['GET'])
def get(id):
    person = Person.query.get(id)
    if person is None:
        return "Não foi encontrado nenhum registro com essa id!"
    result = {
        'id': person.id,
        'name': person.name,
        'email': person.email
    }

    return jsonify(result)


@app.route('/person/<id>', methods=['PUT'])
def update(id):
    person = Person.query.get(id)
    if person is None:
        return "Não foi encontrado nenhum registro com essa id!"
    person.name = request.json['name']
    person.email = request.json['email']

    db.session.commit()
    return "Cadastro atulizado com sucesso!"


@app.route('/person/<id>', methods=['DELETE'])
def delete(id):
    person = Person.query.get(id)
    if person is None:
        return "Não foi encontrado nenhum registro com essa id!"
    db.session.delete(person)
    db.session.commit()

    return "Registro deletado com sucesso!"

