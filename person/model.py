from app import db


class Person(db.Model):
    from debts.model import Debt
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    debts = db.relationship('Debt', backref='person', lazy=True)


    def __init__(self, request):
        self.name = request.json['name']
        self.email = request.json['email']


    def update(self, request):
        self.name = request.json['name']
        self.email = request.json['email']

    def get_as_dict(self):
        person = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        return person

