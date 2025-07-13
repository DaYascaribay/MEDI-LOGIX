from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required, get_jwt
from models import User
from extensions import db
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_panel():
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return "Acceso denegado", 403
    return render_template("admin.html")

@admin_bp.route("/api/admin/medicos", methods=["GET"])
@jwt_required()
def obtener_medicos():
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return jsonify({"mensaje": "Acceso denegado"}), 403

    medicos = User.query.filter_by(rol="medico").all()
    resultado = [
        {
            "id": m.id,
            "usuario": m.usuario,
            "password": m.password,
            "correo": m.correo or "",
            "nombre": m.nombre or "",
            "apellido": m.apellido or "",
            "telefono": m.telefono or "",
            "fecha_nac": m.fecha_nac.strftime("%Y-%m-%d") if m.fecha_nac else "",
            "especialidad": m.especialidad or ""
        } for m in medicos
    ]
    return jsonify(resultado)


@admin_bp.route("/api/admin/crear_medico", methods=["POST"])
@jwt_required()
def crear_medico():
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return jsonify({"mensaje": "Acceso denegado"}), 403

    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    especialidad = data.get("especialidad")
    fecha_nac = data.get("fecha_nac")
    telefono = data.get("telefono")

    if not all([usuario, password, nombre, apellido, correo, especialidad, fecha_nac, telefono]):
        return jsonify({"mensaje": "Faltan campos"}), 400

    if User.query.filter_by(usuario=usuario).first():
        return jsonify({"mensaje": "El usuario ya existe"}), 409

    nuevo_medico = User(
        usuario=usuario,
        password=generate_password_hash(password),
        rol="medico",
        nombre=nombre,
        apellido=apellido,
        correo=correo,
        especialidad=especialidad,
        fecha_nac=fecha_nac,
        telefono=telefono
    )

    db.session.add(nuevo_medico)
    db.session.commit()
    return jsonify({"mensaje": "Médico registrado correctamente"}), 201

@admin_bp.route("/api/admin/medico/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_medico(id):
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return jsonify({"mensaje": "Acceso denegado"}), 403

    medico = User.query.get(id)
    if not medico or medico.rol != "medico":
        return jsonify({"mensaje": "Médico no encontrado"}), 404

    data = request.get_json()
    medico.nombre = data.get("nombre", medico.nombre)
    medico.apellido = data.get("apellido", medico.apellido)
    medico.correo = data.get("correo", medico.correo)
    medico.telefono = data.get("telefono", medico.telefono)
    medico.especialidad = data.get("especialidad", medico.especialidad)
    medico.fecha_nac = data.get("fecha_nac", medico.fecha_nac)

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
    if claims.get("rol") != "admin":
        return jsonify({"mensaje": "Acceso denegado"}), 403

    medico = User.query.get(id)
    if not medico or medico.rol != "medico":
        return jsonify({"mensaje": "Médico no encontrado"}), 404

    try:
        db.session.delete(medico)
        db.session.commit()
        return jsonify({"mensaje": "Médico eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": f"Error al eliminar médico: {str(e)}"}), 500
