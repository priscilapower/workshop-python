from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from appconfig import flask_config


debt = flask_config(__name__)
db = SQLAlchemy(debt)


class Debt(db.Model):
    debt_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    debt_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, person_id, valor, debt_status):
        self.person_id = person_id
        self.person = person_id
        self.valor = valor
        self.debt_status = debt_status


db.create_all()
db.session.commit()


@debt.route('/debt', methods=['POST'])
def insert():
    person_id = request.json['person_id']
    value = request.json['value']
    debt_status = request.json['debt_status']

    debt = Debt(person_id, value, debt_status)
    db.session.add(debt)
    db.session.commit()

    return 'Divida cadastrada!'
