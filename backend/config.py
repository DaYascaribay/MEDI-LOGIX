import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'medilogix140725')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:123456@mysql/historias_clinicas"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'medilogix140725')
