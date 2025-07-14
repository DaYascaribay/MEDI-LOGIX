from flask import Flask
from config import Config
from extensions import db, jwt
from flask_cors import CORS
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def activar_claves_foraneas_sqlite(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):  # Solo para SQLite
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def create_app(test_config=None):
    app = Flask(__name__)

    # Si se pasa una configuración para test, úsala
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from routes.auth_routes import auth_bp
    from routes.patient_routes import patient_bp
    from routes.case_routes import case_bp
    from routes.admin_routes import admin_bp  

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(case_bp, url_prefix="/api/case")
    app.register_blueprint(admin_bp)


    return app


# Ejecutar servidor directamente
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=777)
