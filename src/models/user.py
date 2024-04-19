from .. import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Clase que representa la entidad User en la base de datos

    param:
        - db.Model: Clase de la cual hereda para mapear la entidad.
    """

    __tablename__ = "users"
    __id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    __name = db.Column("name", db.String(50), nullable=False)
    __surname = db.Column("surname", db.String(50), nullable=False)
    __dni = db.Column("dni", db.Integer(8), nullable=False)
    __password = db.Column("password", db.String(255), nullable=False)
    __phone = db.Column("phone", db.String(50), nullable=False)
    __email = db.Column("email", db.String(50), nullable=False)
    __role = db.Column("role", db.String(20), nullable=False)

    # Relacion con Events
    events = db.relationship(
        "Events", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"< User:  {self.__id} {self.__name} {self.__surname} {self.__dni} {self.__phone} {self.__email} {self.__role}>"

    @property
        def plain_password(self):
            raise AttributeError ("Not Allowed")

    @plain_password.setter
    def plain_password(self, password):
        self.passw = generate_password_hash(password)
    
    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    @hybrid_property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @id.deleter
    def id(self):
        del self.__id

    @hybrid_property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        del self.__name

    @hybrid_property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname):
        self.__surname = surname

    @surname.deleter
    def surname(self):
        del self.__surname

    @hybrid_property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, dni):
        self.__dni = dni

    @dni.deleter
    def dni(self):
        del self.__dni

    @hybrid_property
    def password(self):
        return self.__password

    @hybrid_property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @phone.deleter
    def phone(self):
        del self.__phone

    @hybrid_property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @email.deleter
    def email(self):
        del self.__email

    @hybrid_property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @role.deleter
    def role(self):
        del self.__role
