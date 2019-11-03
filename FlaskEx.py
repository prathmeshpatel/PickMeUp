from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # 3 slashes relative, 4 slashes absolute
app.config['DEBUG'] = True

db = SQLAlchemy(app)


class User(db.Model):
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)


@app.route('/')
def main():
    return 'Hello World!'


@app.route('/<name>/<location>')
def index(name, location):
    user = User(name=name, location=location)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added New User!</h1>'


@app.route('/<name>')
def get_user(name):
    user = User.query.filter_by(name=name).first()
    return f'<h1>The user is located in: { user.location }</h1>'
