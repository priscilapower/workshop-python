from flask_sqlalchemy import SQLAlchemy
from config import flask_config, table_creator

app = flask_config(__name__)
db = SQLAlchemy(app)


table_creator()
from person import routes
from debts import routes

if __name__ == '__main__':
    print('Application Runner')
