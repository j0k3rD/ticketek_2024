from .. import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime


class Event(db.Model):
    """
    Clase que representa la entidad Event en la base de datos

    param:
        - db.Model: Clase de la cual hereda para mapear la entidad.
    """

    __tablename__ = "events"
    __id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    __date = db.Column("date", db.DateTime(), default=datetime.now(), nullable=False)
    __name = db.Column("name", db.String(50), nullable=False)
    __description = db.Column("description", db.String(100), nullable=False)
    __location = db.Column("location", db.String(50), nullable=False)
    __capacity = db.Column("capacity", db.Integer(5), nullable=False)
    __organizer = db.Column("organizer", db.String(50), nullable=False)

    # Relacion con User
    users = db.relationship(
        "Users", back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"< User: {self.__id} {self.__date} {self.__name} {self.__description} {self.__location} {self.__capacity} {self.__organizer}>"

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
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @date.deleter
    def date(self):
        del self.__date

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
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @description.deleter
    def description(self):
        del self.__description

    @hybrid_property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location

    @location.deleter
    def location(self):
        del self.__location

    @hybrid_property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity):
        self.__capacity = capacity

    @capacity.deleter
    def capacity(self):
        del self.__capacity

    @hybrid_property
    def organizer(self):
        return self.__organizer

    @organizer.setter
    def organizer(self, organizer):
        self.__organizer = organizer

    @organizer.deleter
    def organizer(self):
        del self.__organizer
