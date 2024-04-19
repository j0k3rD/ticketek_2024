import os

# Each Flask web application contains a secret key which used to sign session cookies for protection against cookie data tampering.
SECRET_KEY = os.urandom(22)

basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode, that will refresh the page when you make changes.
DEBUG = True

# URL de configuracion de base de datos
SQLALCHEMY_DATABASE_URI = (
    "sqlite:////" + os.getenv("DATABASE_PATH") + os.getenv("DATABASE_NAME")
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Cargar clave secreta de JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# Cargar tiempo de expiracion de los tokens JWT
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))

MAIL_HOSTNAME = os.getenv("MAIL_HOSTNAME")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
FLASKY_MAIL_SENDER = os.getenv("FLASKY_MAIL_SENDER")
