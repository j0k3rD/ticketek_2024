<h1 align="center"> TICKETEK 2024 </h1>

## Descripción
Ticketek 2024 es una aplicación web que permite a los usuarios comprar y vender entradas para eventos de todo tipo. La aplicación permite a los administradores crear eventos y validar inscripciones, y a los usuarios crear inscripciones para los eventos.


## Instalación
### 1.  Para instalar el proyecto, primero clone el repositorio en su máquina local:

```bash
git clone git@github.com:j0k3rD/ticketek_2024.git
```

### 2.  Luego, de permisos de ejecución al archivo `install.sh` y al `boot.sh`:

```bash
chmod +x install.sh boot.sh
```

### 3.  Genere un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```bash
DATABASE_URL=sqlite:///./ticketek.db
TEST_DATABASE_URL=sqlite:///:memory:

SECRET_KEY = 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
REFRESH_TOKEN_EXPIRE_MINUTES = 3600

ADMIN_EMAIL = 
ADMIN_EMAIL_PASSWORD=

API_KEY = 
```

(La `API_KEY` es la clave de la API de Google Maps, que se utiliza para obtener la ubicación de los eventos. El `ADMIN_EMAIL` y `ADMIN_EMAIL_PASSWORD` son las credenciales de la cuenta de correo electrónico que se utiliza para enviar correos electrónicos a los usuarios.)


### 4.  Ejecute el script `install.sh` para instalar las dependencias del proyecto:

```bash
./install.sh
```

### 5.  Finalmente, ejecute el script `boot.sh` para iniciar el servidor:

```bash
./boot.sh
```

## Uso
Para acceder a la documentación de la API, abra un navegador web y vaya a la dirección `http://localhost:5000/docs`.

(Para realizar acciones como administrador, tendrá que modificar los routes y descomentar las líneas de código que permiten realizar acciones como administrador.)

## Integrantes
- [García Ezequiel](https://github.com/Ezeg914)
- [Rosales Bruno](https://github.com/bruno212121)
- [Moya Aarón](https://github.com/j0k3rD)

## About

Tecnologías y herramientas utilizadas en el desarrollo de este proyecto:

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) ![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) ![GoogleMaps](https://img.shields.io/badge/GoogleMaps-4285F4?style=for-the-badge&logo=googlemaps&logoColor=white) ![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)

</div>

