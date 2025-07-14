import pytest
from main import create_app
from extensions import db
from models import Medico
from flask_jwt_extended import create_access_token
from datetime import date
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="module")
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "testsecret"
    })

    with app.app_context():
        db.create_all()

        # Crear un usuario administrador
        admin = Medico(
            cedula="0000000000",
            nombres="Admin",
            apellidos="Test",
            correo="admin@test.com",
            usuario="admin",
            contrasena=generate_password_hash("admin123"),
            rol=True,
            especialidad="Admin",
            fecha_nacimiento=date(1990, 1, 1),
            telefono="0000000000"
        )
        db.session.add(admin)
        db.session.commit()

        # Generar token dentro del contexto
        token = create_access_token(identity=str(admin.id_medico), additional_claims={"rol": True})


        # Crear cliente con token ya incluido en headers
        client = app.test_client()
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

        yield client
