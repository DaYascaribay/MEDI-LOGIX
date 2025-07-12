from extensions import db
from models import User
from app import create_app
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    usuario = "admin2"
    contraseña = "1234"
    rol = "admin"

    if User.query.filter_by(usuario=usuario).first():
        print("El usuario ya existe.")
    else:
        nuevo = User(
            usuario=usuario,
            password=generate_password_hash(contraseña),
            rol=rol,
            nombre="Admin",
            apellido="Uno",
            correo="admin1@medilogix.com",
            especialidad="General",
            fecha_nac=datetime.strptime("1980-01-01", "%Y-%m-%d"),
            telefono="0999999999"
        )
        db.session.add(nuevo)
        db.session.commit()
        print("Usuario creado: admin1 / 1234")


    usuario = "doctor1"
    contraseña = "1234"
    rol = "medico"

    if User.query.filter_by(usuario=usuario).first():
        print("El usuario ya existe.")
    else:
        nuevo = User(
            usuario=usuario,
            password=generate_password_hash(contraseña),
            rol=rol
        )
        db.session.add(nuevo)
        db.session.commit()
        print("Usuario creado: admin1 / 1234")