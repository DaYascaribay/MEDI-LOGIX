from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('user')
    password = data.get('password')

    if not username or not password:
        return jsonify({"mensaje": "Usuario y contraseña son obligatorios"}), 400

    user = User.query.filter_by(usuario=username).first()

    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=str(user.id))  # SOLO el ID como string
        return jsonify({
            "token": token,
            "mensaje": "Acceso exitoso"
        }), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
