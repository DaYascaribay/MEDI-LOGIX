from extensions import db
from app import create_app
from models import *

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de datos y tablas creadas.")
