import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flasgger import Swagger

# Inicializar API de Flask-Restful
api = Api()
# Inicializar SQLAlchemy
db = SQLAlchemy()
# Inicializar JWT
jwt = JWTManager()
# Inicializo Email
mailsender = Mail()


def create_app():
    # Inicializar Flask
    app = Flask(__name__)

    # Inicializamos Swagger
    swagger = Swagger(app)

    # Cargar archivo config.py
    app.config.from_object("config")

    load_dotenv()

    # DB
    if not os.path.exists(os.getenv("DATABASE_PATH") + os.getenv("DATABASE_NAME")):
        os.mknod(os.getenv("DATABASE_PATH") + os.getenv("DATABASE_NAME"))

    # Inicia la base de datos
    db.init_app(app)

    # Importar diccionario de Recursos

    # Iniciar JWT
    jwt.init_app(app)

    from main.auth import routes

    # app.register_blueprint(routes.auth)

    mailsender.init_app(app)

    api.init_app(app)
    return app
