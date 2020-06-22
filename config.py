DATABASE_URI = 'mysql+pymysql://root:MySql2020!@localhost:3307/workshop-python'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEY = False


def flask_config(name):
    from flask import Flask
    flask = Flask(name)
    flask.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    flask.config['JSON_SORT_KEYS'] = JSON_SORT_KEY
    return flask


def table_creator():
    from app import db
    from person.model import Person
    from debts.model import Debt
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    print('Application Configuration script')
