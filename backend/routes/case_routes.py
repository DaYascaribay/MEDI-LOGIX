from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import CasoClinico, Medico
from extensions import db
from datetime import datetime

case_bp = Blueprint('case', __name__)

@case_bp.route('/register', methods=['POST'])
@jwt_required()
def register_case():
    try:
        data = request.get_json()
        user_id = int(get_jwt_identity())

        nuevo_caso = CasoClinico(
            id_paciente = data['paciente_id'],  # CORREGIDO
            id_medico = user_id,                # CORREGIDO
            fecha_atencion = datetime.strptime(data['fecha_atencion'], '%Y-%m-%d'),
            diagnostico = data['diagnostico'],
            tratamiento = data['tratamiento'],
            observaciones = data.get('observaciones', '')
        )

        db.session.add(nuevo_caso)
        db.session.commit()

        return jsonify({"mensaje": "Caso clínico registrado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al registrar el caso: {str(e)}"}), 500


@case_bp.route('/list/<int:paciente_id>', methods=['GET'])
@jwt_required()
def listar_casos_por_paciente(paciente_id):
    try:
        casos = CasoClinico.query.filter_by(id_paciente=paciente_id).all()
        resultado = [
            {
                "fecha": caso.fecha_atencion.strftime('%Y-%m-%d'),
                "diagnostico": caso.diagnostico,
                "medico": f"{caso.medico.nombres} {caso.medico.apellidos}" if caso.medico else "Desconocido",
                "tratamiento": caso.tratamiento,
                "observaciones": caso.observaciones
            }
            for caso in casos
        ]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al obtener casos: {str(e)}"}), 500
