from extensions import db
from datetime import datetime

# Tabla MÉDICO
class Medico(db.Model):
    __tablename__ = 'medicos'

    id_medico = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    especialidad = db.Column(db.String(30), nullable=False)
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Boolean, default=False) 
    telefono = db.Column(db.String(10), nullable=True)
    activo = db.Column(db.Boolean, default=True) 
    casos = db.relationship('CasoClinico', backref='medico', lazy=True, cascade="all, delete-orphan")


# Tabla PACIENTE
class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id_paciente = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)  # 'M' o 'F'. Alternativa: usar db.Boolean o db.Integer
    telefono = db.Column(db.String(10), unique=True, nullable=True)
    correo = db.Column(db.String(50), unique=True, nullable=True)

    casos = db.relationship('CasoClinico', backref='paciente', lazy=True, cascade="all, delete-orphan")


# Tabla CASO CLÍNICO
class CasoClinico(db.Model):
    __tablename__ = 'casos_clinicos'

    id_caso = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id_medico'), nullable=False)
    fecha_atencion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnostico = db.Column(db.String(300), nullable=False)
    tratamiento = db.Column(db.String(300), nullable=False)
    observaciones = db.Column(db.String(200), nullable=True)
