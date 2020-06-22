from flask import request, jsonify
from .model import Debt
from person.model import Person
from app import app, db


@app.route('/debt', methods=['GET'])
def index_debt():
    debts = Debt.query.all()
    if debts is None:
        return jsonify(error='Nenhum divida foi encontrada!')

    result = []
    for debt in debts:
        result.append(debt.get_as_dict())
    return jsonify(result)


@app.route('/debt/<id>', methods=['GET'])
def get_debt(id):
    debt = Debt.query.get(id)
    if debt is None:
        return id_not_found(id)

    return jsonify(debt.get_as_dict())


@app.route('/debt', methods=['POST'])
def insert_debt():
    person = Person.query.get(request.json['person_id'])
    if person is None:
        return jsonify(error='Não foi possivel cadastrar nenhuma divida pois'
                             ' não existe nenhuma pessoa com esse id')

    debt = Debt(request)
    db.session.add(debt)
    db.session.commit()

    return jsonify(sucess='Divida cadastrada com sucesso!')


@app.route('/debt/<id>', methods=['PUT'])
def update_debt(id):
    debt = Debt.query.get(id)
    if debt is None:
        return id_not_found(id)

    debt.update(request)
    db.session.commit()

    return jsonify(sucess='Divida atualizada com sucesso')


@app.route('/debt/<id>', methods=['DELETE'])
def delete_debt(id):
    debt = Debt.query.get(id)
    if debt is None:
        return id_not_found(id)

    db.session.delete(debt)
    db.session.commit()

    return jsonify(sucess='Divida deletada com sucesso!')


@app.route('/debt/<id>/pay', methods=['POST'])
def pay_debt(id):
    debt = Debt.query.get(id)
    if debt is None:
        return id_not_found(id)

    is_payed = debt.debt_status
    if is_payed:
        return jsonify(error='Essa divida já foi paga!')
    else:
        debt.debt_status = True
        db.session.commit()
        return jsonify(sucess='Divida paga com sucesso!')


def get_payed_by_person(id):
    debts = db.session.query(Debt).filter(Debt.person_id == id).filter(Debt.debt_status == True)
    result = []

    for debt in debts:
        result.append(debt.get_as_dict())
    if len(result) == 0:
        return 'Não possui nenhuma divida paga!'

    return result


def get_by_person(id):
    debts = db.session.query(Debt).filter(Debt.person_id == id)
    result = []

    for debt in debts:
        result.append(debt.get_as_dict())
    if len(result) == 0:
        return 'Não possui nenhuma divida!'

    return result


def id_not_found(id):
    return jsonify(error=f'Nenhum divida foi encontrada com esse ID! - ID={id}')
