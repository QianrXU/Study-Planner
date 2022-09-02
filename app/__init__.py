from distutils.log import debug
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

app = Flask(__name__)

app.secret_key = 'this1sKey'

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'


from app import routes, models, forms

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

