from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'admin'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySql2020!@localhost/workshop-python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
