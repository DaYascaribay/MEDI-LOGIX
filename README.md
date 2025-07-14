# MediLogix 🏥 – Historial Médico con Flask + MySQL + Docker

Este proyecto gestiona pacientes y casos médicos usando Flask y una base de datos MySQL contenida en Docker.

---

## 🚀 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.10+ instalado localmente

---

## 🛠️ Tecnologías Usadas

- **Backend:**
  - **Flask:** Un microframework de Python ligero para construir aplicaciones web.
  - **Flask-SQLAlchemy:** Facilita la interacción con bases de datos SQL.
  - **Flask-JWT-Extended:** Para gestionar la autenticación mediante JSON Web Tokens (JWT).
  - **Flask-Cors:** Permite peticiones Cross-Origin Resource Sharing (CORS) para APIs.
- **Base de Datos:**
  - **MySQL:** Como sistema de gestión de bases de datos, dockerizado para portabilidad.
  - **Docker & Docker Compose:** Para crear, desplegar y gestionar la aplicación en contenedores.
- **Frontend (Básico):**
  - **HTML/CSS:** Para la estructura y el estilo de las vistas.

---

## 📂 Estructura de Archivos

```
medilogix/
│
├── backend/
│   ├── Dockerfile             # Define la imagen de Docker para el backend de Flask.
│   ├── docker-compose.yml     # Orquesta los servicios de la aplicación (backend y base de datos).
│   ├── requirements.txt       # Lista de dependencias de Python.
│   ├── main.py                # Punto de entrada de la aplicación Flask.
│   ├── config.py              # Configuraciones de la aplicación (ej. claves secretas).
│   ├── extensions.py          # Inicialización de extensiones de Flask (ej. SQLAlchemy).
│   ├── models.py              # Define los modelos de la base de datos.
│   ├── create_db.py           # Script para inicializar la base de datos.
│   ├── seed.py                # Script para poblar la base de datos con datos iniciales.
│   └── routes/                # Contiene los blueprints de las rutas de la API.
│       ├── auth_routes.py
│       ├── patient_routes.py
│       └── ...
│
├── static/
│   ├── style.css              # Estilos CSS.
│   └── ...
│
├── templates/
│   ├── index.html             # Plantillas HTML para las vistas.
│   └── ...
│
└── README.md                  # Este archivo.
```

---

## ⚙️ Cómo se Ejecuta

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu_usuario/medilogix.git
   cd medilogix
   ```

2. **Levanta los contenedores con Docker Compose**
   Desde la carpeta `backend`, ejecuta:
   ```bash
   docker-compose up --build
   ```
   Esto construirá la imagen de Flask y levantará tanto el servicio del backend como el de la base de datos.

3. **Inicializa la base de datos (solo la primera vez)**
   Abre otra terminal y, desde la carpeta `backend`, ejecuta:
   ```bash
   docker-compose exec backend python create_db.py
   ```

4. **Puebla la base de datos con datos de prueba (opcional)**
   ```bash
   docker-compose exec backend python seed.py
   ```

5. **Accede a la aplicación**
   - La API del backend estará disponible en `http://localhost:777`.
   - Las vistas web se pueden acceder desde `http://localhost:5000` (si estás corriendo `app.py` localmente fuera de Docker).

---

## 🧪 Pruebas Unitarias

Para asegurar la calidad y el correcto funcionamiento de la aplicación, se han implementado pruebas unitarias con `pytest`.

### Cómo Ejecutar las Pruebas

1. **Asegúrate de que los contenedores estén en ejecución.**
   ```bash
   docker-compose up -d
   ```

2. **Ejecuta los tests**
   Desde la carpeta `backend`, utiliza el siguiente comando para correr las pruebas dentro del contenedor de Flask:
   ```bash
   docker exec -it flask_backend pytest
   ```
   `pytest` descubrirá y ejecutará automáticamente las pruebas definidas en el directorio `backend/tests`.
