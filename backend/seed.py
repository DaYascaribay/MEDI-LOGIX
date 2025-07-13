from main import create_app
from extensions import db
from models import Medico, Paciente, CasoClinico
from datetime import datetime
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Crear admin
    if not Medico.query.filter_by(usuario="admin").first():
        admin = Medico(
            cedula="0000000000",  # ← agregado
            nombres="Admin",
            apellidos="General",
            correo="admin@medilogix.com",
            fecha_nacimiento=datetime(1980, 1, 1),
            especialidad="Administrador",
            usuario="admin",
            contrasena=generate_password_hash("admin123"),
            rol=True,
            telefono="0999999999"
        )
        db.session.add(admin)

    # Crear médico
    if not Medico.query.filter_by(usuario="drmario").first():
        medico = Medico(
            cedula="1101234567",  # ← agregado
            nombres="Mario",
            apellidos="Romero",
            correo="mario.romero@hospital.com",
            fecha_nacimiento=datetime(1990, 6, 15),
            especialidad="Pediatría",
            usuario="drmario",
            contrasena=generate_password_hash("mario123"),
            rol=False,
            telefono="0912345678"
        )
        db.session.add(medico)
        db.session.commit()  # para que tenga id_medico asignado

        # Crear paciente
        paciente = Paciente(
            cedula="1102233445",
            nombres="Juana",
            apellidos="Pérez",
            fecha_nacimiento=datetime(2000, 5, 20),
            sexo="F",
            telefono="0987654321",
            correo="juana.perez@example.com"
        )
        db.session.add(paciente)
        db.session.commit()

        # Crear caso clínico asociado
        caso = CasoClinico(
            id_paciente=paciente.id_paciente,
            id_medico=medico.id_medico,
            fecha_atencion=datetime.now(),
            diagnostico="Faringitis aguda",
            tratamiento="Antibióticos y reposo",
            observaciones="Paciente respondió bien al tratamiento inicial"
        )
        db.session.add(caso)

    db.session.commit()
    print("✅ Admin, médico, paciente y caso clínico creados correctamente.")
