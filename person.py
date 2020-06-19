from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from appconfig import flask_config

person = flask_config(__name__)
db = SQLAlchemy(person)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    debt = db.relationship("Debt", backref='person', lazy=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email


db.create_all()
db.session.commit()


@person.route('/person', methods=['GET'])
def index():
    people = Person.query.all()

    result = []
    for person in people:
        data = {
            'id': person.id,
            'name': person.name,
            'email': person.email
        }
        result.append(data)
    return jsonify(result)


@person.route('/person', methods=['POST'])
def insert():
    name = request.json['name']
    email = request.json['email']

    person = Person(name, email)
    db.session.add(person)
    db.session.commit()

    return "Pessoa inserida com sucesso!"


@person.route('/person/<id>', methods=['GET'])
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


@person.route('/person/<id>', methods=['PUT'])
def update(id):
    person = Person.query.get(id)
    if person is None:
        return "Não foi encontrado nenhum registro com essa id!"
    person.name = request.json['name']
    person.email = request.json['email']

    db.session.commit()
    return "Cadastro atulizado com sucesso!"


@person.route('/person/<id>', methods=['DELETE'])
def delete(id):
    person = Person.query.get(id)
    if person is None:
        return "Não foi encontrado nenhum registro com essa id!"
    db.session.delete(person)
    db.session.commit()

    return "Registro deletado com sucesso!"


if __name__ == '__main__':
    print(__file__)
