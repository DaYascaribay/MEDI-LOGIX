from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Paciente
from extensions import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/add', methods=['POST'])
@jwt_required()
def add_patient():
    data = request.get_json()
    try:
        # Validar formato de fecha
        try:
            fecha = datetime.strptime(data['fecha_nac'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"mensaje": "Formato de fecha inválido. Use AAAA-MM-DD"}), 422

        paciente = Paciente(
            cedula=data['cedula'],
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            fecha_nacimiento=fecha,
            sexo=data['sexo'],
            telefono=data.get('telefono', '')
        )

        db.session.add(paciente)
        db.session.commit()
        return jsonify({
            "mensaje": "Paciente registrado correctamente",
            "id": paciente.id_paciente  # CORREGIDO
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"mensaje": "Ya existe un paciente con esa cédula"}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al registrar paciente: {str(e)}"}), 500


@patient_bp.route('/list', methods=['GET'])
@jwt_required()
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = [
        {
            "id": p.id_paciente,  # CORREGIDO
            "cedula": p.cedula,
            "nombres": p.nombres,
            "apellidos": p.apellidos,
            "fecha_nacimiento": p.fecha_nacimiento.strftime('%Y-%m-%d'),
            "sexo": p.sexo,
            "telefono": p.telefono
        } for p in pacientes
    ]
    return jsonify(resultado)


@patient_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({"mensaje": "Paciente eliminado"})


@patient_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404

    data = request.get_json()
    try:
        paciente.telefono = data.get('telefono', paciente.telefono)
        paciente.sexo = data.get('sexo', paciente.sexo)
        paciente.nombres = data.get('nombres', paciente.nombres)
        paciente.apellidos = data.get('apellidos', paciente.apellidos)
        paciente.fecha_nacimiento = datetime.strptime(data.get('fecha_nacimiento', paciente.fecha_nacimiento.strftime('%Y-%m-%d')), '%Y-%m-%d')
        db.session.commit()
        return jsonify({"mensaje": "Datos del paciente actualizados"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al actualizar: {str(e)}"}), 500


@patient_bp.route('/search/<cedula>', methods=['GET'])
@jwt_required()
def buscar_por_cedula(cedula):
    paciente = Paciente.query.filter_by(cedula=cedula).first()
    if not paciente:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404
    return jsonify({
        "id": paciente.id_paciente,  # CORREGIDO
        "cedula": paciente.cedula,
        "nombres": paciente.nombres,
        "apellidos": paciente.apellidos,
        "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
        "sexo": paciente.sexo,
        "telefono": paciente.telefono
    })
