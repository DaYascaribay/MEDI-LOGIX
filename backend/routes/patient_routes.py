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

        # Validar edad máxima
        hoy = datetime.now().date()
        edad = (hoy - fecha.date()).days // 365
        if edad > 120:
            return jsonify({"mensaje": "La edad del paciente no puede superar los 120 años"}), 422

        # Verificar duplicados
        if Paciente.query.filter_by(cedula=data['cedula']).first():
            return jsonify({"mensaje": "Ya existe un paciente con esa cédula"}), 409
        if data.get('correo') and Paciente.query.filter_by(correo=data['correo']).first():
            return jsonify({"mensaje": "Ya existe un paciente con ese correo"}), 409
        if data.get('telefono') and Paciente.query.filter_by(telefono=data['telefono']).first():
            return jsonify({"mensaje": "Ya existe un paciente con ese teléfono"}), 409

        paciente = Paciente(
            cedula=data['cedula'],
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            fecha_nacimiento=fecha,
            sexo=data['sexo'],
            telefono=data.get('telefono', ''),
            correo=data.get('correo', '')
        )

        db.session.add(paciente)
        db.session.commit()
        return jsonify({
            "mensaje": "Paciente registrado correctamente",
            "id": paciente.id_paciente
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al registrar paciente: {str(e)}"}), 500

@patient_bp.route('/list', methods=['GET'])
@jwt_required()
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = [
        {
            "id": p.id_paciente,
            "cedula": p.cedula,
            "nombres": p.nombres,
            "apellidos": p.apellidos,
            "fecha_nac": p.fecha_nacimiento.strftime('%Y-%m-%d'),
            "sexo": p.sexo,
            "telefono": p.telefono,
            "correo": p.correo or "",
            "historia_clinica": f"HC-{p.id_paciente:05d}"  # ← FORMATO 00001
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
        nuevo_correo = data.get('correo')
        nuevo_telefono = data.get('telefono')

        # Verificar duplicados
        if nuevo_correo:
            existente = Paciente.query.filter_by(correo=nuevo_correo).first()
            if existente and existente.id_paciente != paciente.id_paciente:
                return jsonify({"mensaje": "Ya existe un paciente con ese correo"}), 409

        if nuevo_telefono:
            existente = Paciente.query.filter_by(telefono=nuevo_telefono).first()
            if existente and existente.id_paciente != paciente.id_paciente:
                return jsonify({"mensaje": "Ya existe un paciente con ese teléfono"}), 409

        # Validar edad máxima si se cambia la fecha
        fecha_str = data.get('fecha_nacimiento')
        if fecha_str:
            try:
                nueva_fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({"mensaje": "Formato de fecha inválido. Use AAAA-MM-DD"}), 422

            hoy = datetime.now().date()
            edad = (hoy - nueva_fecha.date()).days // 365
            if edad > 120:
                return jsonify({"mensaje": "La edad del paciente no puede superar los 120 años"}), 422

            paciente.fecha_nacimiento = nueva_fecha

        paciente.telefono = nuevo_telefono or paciente.telefono
        paciente.sexo = data.get('sexo', paciente.sexo)
        paciente.nombres = data.get('nombres', paciente.nombres)
        paciente.apellidos = data.get('apellidos', paciente.apellidos)
        paciente.correo = nuevo_correo or paciente.correo

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
        "id": paciente.id_paciente,
        "cedula": paciente.cedula,
        "nombres": paciente.nombres,
        "apellidos": paciente.apellidos,
        "fecha_nac": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
        "sexo": paciente.sexo,
        "telefono": paciente.telefono,
        "correo": paciente.correo or "",
        "historia_clinica": f"HC-{paciente.id_paciente:05d}"  # ← FORMATO 00001
    })
