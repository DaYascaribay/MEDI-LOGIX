from extensions import db
from models import User
from app import create_app
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    usuario = "admin1"
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
