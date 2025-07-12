from flask import Flask
from config import Config
from extensions import db, jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    # Registro de Blueprints
    from routes.auth_routes import auth_bp
    from routes.patient_routes import patient_bp
    from routes.case_routes import case_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(case_bp, url_prefix="/api/case")

    return app

# Entry point para Docker
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=777)
