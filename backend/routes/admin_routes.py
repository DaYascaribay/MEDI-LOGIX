from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required, get_jwt
from models import Medico
from extensions import db
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_panel():
    claims = get_jwt()
    if not claims.get("rol"):  # rol=True es admin
        return "Acceso denegado", 403
    return render_template("admin.html")


@admin_bp.route("/api/admin/medicos", methods=["GET"])
@jwt_required()
def obtener_medicos():
    claims = get_jwt()
    if not claims.get("rol"):
        return jsonify({"mensaje": "Acceso denegado"}), 403

    try:
        medicos = Medico.query.filter_by(rol=False).all()
        resultado = [
            {
                "id": m.id_medico,
                "usuario": m.usuario,
                "contrasena": m.contrasena,
                "correo": m.correo or "",
                "nombres": m.nombres or "",
                "apellidos": m.apellidos or "",
                "telefono": m.telefono or "",
                "fecha_nacimiento": m.fecha_nacimiento.strftime("%Y-%m-%d") if m.fecha_nacimiento else "",
                "especialidad": m.especialidad or ""
            } for m in medicos
        ]
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Error en /api/admin/medicos: {e}")
        return jsonify({"mensaje": f"Error interno: {str(e)}"}), 500


@admin_bp.route("/api/admin/crear_medico", methods=["POST"])
@jwt_required()
def crear_medico():
    claims = get_jwt()
    if not claims.get("rol"):
        return jsonify({"mensaje": "Acceso denegado"}), 403

    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    correo = data.get("correo")
    especialidad = data.get("especialidad")
    fecha_nacimiento = data.get("fecha_nacimiento")
    telefono = data.get("telefono")

    if not all([usuario, password, nombres, apellidos, correo, especialidad, fecha_nacimiento, telefono]):
        return jsonify({"mensaje": "Faltan campos"}), 400

    if Medico.query.filter_by(usuario=usuario).first():
        return jsonify({"mensaje": "El usuario ya existe"}), 409

    nuevo_medico = Medico(
        usuario=usuario,
        contrasena=generate_password_hash(password),
        rol=False,
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        especialidad=especialidad,
        fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d"),
        telefono=telefono
    )

    db.session.add(nuevo_medico)
    db.session.commit()
    return jsonify({"mensaje": "Médico registrado correctamente"}), 201


@admin_bp.route("/api/admin/medico/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_medico(id):
    claims = get_jwt()
    if not claims.get("rol"):
        return jsonify({"mensaje": "Acceso denegado"}), 403

    medico = Medico.query.get(id)
    if not medico or medico.rol:
        return jsonify({"mensaje": "Médico no encontrado"}), 404

    data = request.get_json()
    medico.nombres = data.get("nombres", medico.nombres)
    medico.apellidos = data.get("apellidos", medico.apellidos)
    medico.correo = data.get("correo", medico.correo)
    medico.telefono = data.get("telefono", medico.telefono)
    medico.especialidad = data.get("especialidad", medico.especialidad)

    fecha_nacimiento = data.get("fecha_nacimiento")
    if fecha_nacimiento:
        try:
            medico.fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        except:
            pass

    try:
        db.session.commit()
        return jsonify({"mensaje": "Médico actualizado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error: {str(e)}"}), 500


@admin_bp.route("/api/admin/medico/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_medico(id):
    claims = get_jwt()
    if not claims.get("rol"):
        return jsonify({"mensaje": "Acceso denegado"}), 403

    medico = Medico.query.get(id)
    if not medico or medico.rol:
        return jsonify({"mensaje": "Médico no encontrado"}), 404

    try:
        db.session.delete(medico)
        db.session.commit()
        return jsonify({"mensaje": "Médico eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al eliminar médico: {str(e)}"}), 500


@admin_bp.route("/api/admin/toggle_medico/<int:id>", methods=["PATCH"])
@jwt_required()
def toggle_estado_medico(id):
    claims = get_jwt()
    if not claims.get("rol"):
        return jsonify({"mensaje": "Acceso denegado"}), 403

    medico = Medico.query.get(id)
    if not medico:
        return jsonify({"mensaje": "Médico no encontrado"}), 404

    medico.activo = not medico.activo  # alterna entre True y False
    db.session.commit()
    return jsonify({"mensaje": f"Médico {'habilitado' if medico.activo else 'inhabilitado'} correctamente"}), 200
