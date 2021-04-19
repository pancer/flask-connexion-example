from functools import wraps

import connexion
from flask import request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import jwt
import time

JWT_SECRET = 'MY JWT SECRET'
JWT_LIFETIME_SECONDS = 600000


def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'AUTHORIZATION' in headers:
                    token = headers['AUTHORIZATION'].split(' ')[1]
                    decoded_token = decode_token(token)
                    if 'admin' in decoded_token['roles'] or arg in decoded_token['roles']:
                        return fn(*args, **kwargs)
                    abort(401)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)
        return decorated_view
    return has_role_inner


@has_role('invoice')
def get_test1(test1_id):
    data = request.data
    headers = request.headers
    # token = headers['HTTP_AUTHORIZATION']
    return {'id': 1, 'name': 'name', 'entered_id': test1_id}


def auth(auth_body):
    timestamp = int(time.time())
    user_id = 1
    payload = {
        "iss": 'my app',
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": auth_body['username'],
        "roles": [
            "invoice",
            "social"
        ]
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return encoded


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])


def person_add(person_body):
    new_person = Person(name=person_body['name'], surname=person_body['surname'])
    db.session.add(new_person)
    db.session.commit()


def person_find(person_name):
    found_person = db.session.query(Person).filter_by(name=person_name).first()
    if found_person:
        return { 'id': found_person.id, 'name': found_person.name, 'surname': found_person.surname}
    else:
        return {'error': '{} not found'.format(person_name)}, 404


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

# dummy reference for migrations only
from models import User, Person
from models2 import Person2

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
