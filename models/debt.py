from app import db


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    paid = db.Column(db.Boolean)
    value = db.Column(db.Float)

    def __init__(self, person_id, paid, value):
        self.person_id = person_id
        self.paid = paid
        self.value = value
