from models.person import Person
from flask import request, jsonify
from app import app, db


# Person Routes
@app.route('/person')
def get_all_person():
    people = Person.query.all()

    result = []
    for person in people:
        data = {}
        data['id'] = person.id
        data['name'] = person.name
        data['email'] = person.email

        result.append(data)

    return jsonify(result)


@app.route('/person/<id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)

    result = {
        'id': person.id,
        'name': person.name,
        'email': person.email
    }

    return jsonify(result)


@app.route('/person', methods=['POST'])
def insert_person():
    name = request.json['name']
    email = request.json['email']

    person = Person(name, email)
    db.session.add(person)
    db.session.commit()

    return "Pessoa inserida com sucesso!"


@app.route('/person', methods=['PUT'])
def update_person():
    id = request.json['id']
    person = Person.query.get(id)
    person.name = request.json['name']
    person.email = request.json['email']

    db.session.commit()

    return "Pessoa atualizada com sucesso!"


@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return "Pessoa deletada com sucesso!"