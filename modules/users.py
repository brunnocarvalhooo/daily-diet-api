from flask_login import logout_user, login_required, login_user
from flask import jsonify, request, Blueprint
import bcrypt

from login_manager import login_manager
from models.user import User
from database import db

users = Blueprint('users', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@users.route('/login', methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if email and password:
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            login_user(user)

            return jsonify({"message": "Autenticação realizada com sucesso"})

    return jsonify({"message": "Credenciais inválidas"}), 400


@users.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()

    return jsonify({"message": "Logout realizado com sucesso!"})


@users.route('/', methods=["POST"])
def create_user():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if name and password and email:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

        user = User(name=name, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuario cadastrado com sucesso"})

    return jsonify({"message": "Dados invalidos"}), 400
