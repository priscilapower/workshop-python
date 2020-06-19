from flask import Flask


DATABASE_URI = 'mysql+pymysql://root:MySql2020!@localhost/workshop-python'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEY = False


def flask_config(name):
    flask = Flask(name)
    flask.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    flask.config['JSON_SORT_KEYS'] = JSON_SORT_KEY
    return flask


