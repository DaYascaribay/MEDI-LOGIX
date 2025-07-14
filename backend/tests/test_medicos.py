from datetime import date

def test_crear_medico(client):
    data = {
        "cedula": "1234567890",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "correo": "juan@test.com",
        "password": "1234",
        "especialidad": "Pediatría",
        "fecha_nacimiento": "1990-05-05",
        "telefono": "0999999999"
    }

    response = client.post("/api/admin/crear_medico", json=data)
    assert response.status_code == 201
    assert "registrado" in response.json["mensaje"].lower()


def test_crear_medico_sin_especialidad(client):
    data = {
        "cedula": "1234567891",
        "nombres": "Laura",
        "apellidos": "Torres",
        "correo": "laura@test.com",
        "password": "pass123",
        "fecha_nacimiento": "1985-03-10",
        "telefono": "0988888888"
    }

    response = client.post("/api/admin/crear_medico", json=data)
    assert response.status_code == 400
    assert "faltan" in response.json["mensaje"].lower()


def test_listar_medicos(client):
    response = client.get("/api/admin/medicos")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(m["cedula"] == "1234567890" for m in response.json)


def test_actualizar_medico(client):
    # Obtener un ID de médico existente
    lista = client.get("/api/admin/medicos").json
    id_medico = lista[0]["id"]

    data = {
        "nombres": "Juan Carlos",
        "telefono": "0991111111"
    }

    response = client.put(f"/api/admin/medico/{id_medico}", json=data)
    assert response.status_code == 200
    assert "actualizado" in response.json["mensaje"].lower()


def test_toggle_estado_medico(client):
    lista = client.get("/api/admin/medicos").json
    id_medico = lista[0]["id"]

    response = client.patch(f"/api/admin/toggle_medico/{id_medico}")
    assert response.status_code == 200
    assert "médico" in response.json["mensaje"].lower()
