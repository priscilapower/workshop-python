from flask import request, jsonify
from .model import Person
from debts.routes import get_by_person, get_payed_by_person
from app import app, db


@app.route('/person', methods=['GET'])
def index_person():
    people = Person.query.all()
    if people is None:
        return jsonify(error='Nenhuma pessoa foi encontrada!')

    result = []
    for person in people:
        result.append(person.get_as_dict())
    return jsonify(result)


@app.route('/person/<id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    if person is None:
        return id_not_found(id)

    return jsonify(person.get_as_dict())


@app.route('/person', methods=['POST'])
def insert_person():
    person = Person(request)
    db.session.add(person)
    db.session.commit()

    return jsonify(sucess='Pessoa cadastrada com sucesso!')


@app.route('/person/<id>', methods=['PUT'])
def update_person(id):
    person = Person.query.get(id)
    if person is None:
        return id_not_found(id)

    person.update(request)
    db.session.commit()

    return jsonify(sucess='Cadastro atulizado com sucesso!')


@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    if person is None:
        return id_not_found(id)

    db.session.delete(person)
    db.session.commit()

    return jsonify(sucess='Pessoa deletada com sucesso!')


@app.route('/person/<id>/debt', methods=['GET'])
def person_debts(id):
    person = Person.query.get(id)
    if person is None:
        return id_not_found(id)

    person = get_by_person(id)
    if type(person) == str:
        return person

    return jsonify(person)


@app.route('/person/<id>/payed')
def person_payed_debts(id):
    person = Person.query.get(id)
    if person is None:
        return id_not_found(id)

    debts = get_payed_by_person(id)
    if type(debts) == str:
        return debts

    return jsonify(debts)


@app.route('/person/<id>/info')
def person_info(id):
    person = Person.query.get(id)
    if person is None:
        return id_not_found(id)

    result = {
        'id': person.id,
        'name': person.name,
        'email': person.email,
        'debts': get_by_person(person.id)
    }
    return jsonify(result)


def id_not_found(id):
    return jsonify(error=f'Não foi encontrado nenhuma pessoa com esse ID! ID={id}')
