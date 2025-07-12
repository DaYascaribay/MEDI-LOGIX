from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    # Agregar estas columnas:
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    especialidad = db.Column(db.String(100), nullable=True)
    fecha_nac = db.Column(db.Date, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)



class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    fecha_nac = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    casos = db.relationship('CasoClinico', backref='paciente', lazy=True, cascade="all, delete-orphan")


# models.py

class CasoClinico(db.Model):
    __tablename__ = "casos_clinicos"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    diagnostico = db.Column(db.String(255), nullable=False)
    tratamiento = db.Column(db.String(255), nullable=False)
    observaciones = db.Column(db.Text)
    medico = db.relationship("User", backref="casos")


class Auditoria(db.Model):
    __tablename__ = 'auditoria'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    accion = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    modulo = db.Column(db.String(100), nullable=False)
    detalle = db.Column(db.String(1000))
