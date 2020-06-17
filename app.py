from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'admin'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySql2020!@localhost/workshop-python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    debts = db.relationship('Debt')

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    paid = db.Column(db.Boolean)
    value = db.Column(db.Float)

    def __init__(self, person_id, paid, value):
        self.person_id = person_id
        self.paid = paid
        self.value = value


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
