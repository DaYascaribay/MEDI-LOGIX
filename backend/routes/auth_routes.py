from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import Medico

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('user')
    password = data.get('password')

    if not username or not password:
        return jsonify({"mensaje": "Usuario y contraseña son obligatorios"}), 400

    medico = Medico.query.filter_by(usuario=username).first()

    if medico and medico.activo and check_password_hash(medico.contrasena, password):
        rol_str = "admin" if medico.rol else "medico"

        additional_claims = {
            "rol": rol_str
        }

        token = create_access_token(identity=str(medico.id_medico), additional_claims=additional_claims)

        return jsonify({
            "token": token,
            "rol": rol_str,
            "mensaje": "Acceso exitoso"
        }), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
