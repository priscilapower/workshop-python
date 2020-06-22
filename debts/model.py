from app import db


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    debt_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, request):
        self.person_id = request.json['person_id']
        self.value = request.json['value']
        self.debt_status = request.json['debt_status']


    def update(self, request):
        self.person_id = request.json['person_id']
        self.value = request.json['value']
        self.debt_status = request.json['debt_status']


    def get_as_dict(self):
        debt = {
            'id': self.id,
            'person_id': self.person_id,
            'value': self.value,
            'debt_status': self.debt_status
        }
        return debt
