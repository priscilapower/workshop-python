from models.debt import Debt
from models.person import Person
from flask import request, jsonify
from app import app, db


# Debt Routes
@app.route('/person/debt/<person_id>', methods=['GET'])
def get_person_debts(person_id):
    person = Person.query.get(person_id)

    debts = person_debts(person.debts)

    result = {
        'id': person.id,
        'name': person.name,
        'email': person.email,
        'debts': debts
    }

    return jsonify(result)


@app.route('/debt')
def get_all_debt():
    debts = Debt.query.all()

    result = []
    for debt in debts:
        data = {}
        data['id'] = debt.id
        data['person_id'] = debt.person_id
        data['paid'] = debt.paid
        data['value'] = debt.value

        result.append(data)

    return jsonify(result)


@app.route('/debt/<id>', methods=['GET'])
def get_debt(id):
    debt = Debt.query.get(id)

    result = {
        'id': debt.id,
        'person_id': debt.person_id,
        'paid': debt.paid,
        'value': debt.value
    }

    return jsonify(result)


@app.route('/debt', methods=['POST'])
def insert_debt():
    person_id = request.json['person_id']
    paid = request.json['paid']
    value = request.json['value']

    debt = Debt(person_id, paid, value)
    db.session.add(debt)
    db.session.commit()

    return "Dívida inserida com sucesso!"


@app.route('/debt', methods=['PUT'])
def update_debt():
    id = request.json['id']
    debt = Debt.query.get(id)
    debt.person_id = request.json['person_id']
    debt.paid = request.json['paid']
    debt.value = request.json['value']

    db.session.commit()

    return "Dívida atualizada com sucesso!"


@app.route('/debt/<id>', methods=['DELETE'])
def delete_debt(id):
    debt = Debt.query.get(id)

    db.session.delete(debt)
    db.session.commit()

    return "Dívida deletada com sucesso!"


@app.route('/debt/pay', methods=['PUT'])
def debt_payment():
    id = request.json['id']
    debt = Debt.query.get(id)

    if debt.paid:
        return "A dívida já está paga"
    else:
        debt.paid = True;
    db.session.commit()

    return "Dívida paga com sucesso!"


@app.route('/debt/paid', methods = ['GET'])
def get_paid_debts():
    debts = Debt.query.filter(Debt.paid).all()

    results = person_debts(debts)
    return jsonify(results)


def person_debts(debts):
    result = []

    for debt in debts:
        data = {}

        data['id'] = debt.id
        data['person_id'] = debt.person_id
        data['paid'] = debt.paid
        data['value'] = debt.value

        result.append(data)
    return result
