from datetime import date
import pytest
from models import Medico, Paciente
from extensions import db
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="module")
def client():
    from main import create_app
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "testsecret"
    })

    with app.app_context():
        db.create_all()

        # Crear un médico admin para autenticar
        admin = Medico(
            cedula="0000000000",
            nombres="Admin",
            apellidos="Test",
            correo="admin@test.com",
            usuario="admin",
            contrasena="admin123",
            rol=True,
            especialidad="General",
            fecha_nacimiento=date(1990, 1, 1),
            telefono="0000000000"
        )
        db.session.add(admin)
        db.session.commit()

        token = create_access_token(identity=str(admin.id_medico), additional_claims={"rol": True})
        test_client = app.test_client()
        test_client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        yield test_client


# tests/test_pacientes.py

def test_agregar_paciente(client):
    data = {
        "cedula": "1234567890",
        "nombres": "Pedro",
        "apellidos": "Gómez",
        "fecha_nac": "2000-01-01",
        "sexo": "M",
        "telefono": "0991112233"
    }
    res = client.post("/api/patient/add", json=data)
    assert res.status_code == 201


def test_agregar_paciente_repetido(client):
    data = {
        "cedula": "1234567890",
        "nombres": "Pedro",
        "apellidos": "Gómez",
        "fecha_nac": "2000-01-01",
        "sexo": "M",
        "telefono": "0991112233"
    }
    res = client.post("/api/patient/add", json=data)
    assert res.status_code == 409


def test_agregar_paciente_fecha_invalida(client):
    data = {
        "cedula": "9876543210",
        "nombres": "Laura",
        "apellidos": "Lopez",
        "fecha_nac": "01-01-2000",  # Formato incorrecto
        "sexo": "F",
        "telefono": "0992223344"
    }
    res = client.post("/api/patient/add", json=data)
    assert res.status_code == 422


def test_listar_pacientes(client):
    res = client.get("/api/patient/list")
    assert res.status_code == 200
    assert isinstance(res.json, list)


def test_buscar_paciente_por_cedula(client):
    res = client.get("/api/patient/search/1234567890")
    assert res.status_code == 200
    assert res.json["cedula"] == "1234567890"


def test_actualizar_paciente(client):
    from models import Paciente
    paciente = db.session.query(Paciente).filter_by(cedula="1234567890").first()
    res = client.put(f"/api/patient/update/{paciente.id_paciente}", json={
        "telefono": "000111222",
        "nombres": "Pedro Actualizado"
    })
    assert res.status_code == 200


def test_eliminar_paciente(client):
    from models import Paciente
    paciente = db.session.query(Paciente).filter_by(cedula="1234567890").first()
    res = client.delete(f"/api/patient/delete/{paciente.id_paciente}")
    assert res.status_code == 200
