from src.repositories.repository import Create, Delete, Read, Update
from src.models import EventModel
from .. import db

class EventRepository(Create, Read, Update):
    '''
    Clase que representa el repositorio de la entidad Event

    param:
        - Create: Clase que hereda de la interfaz Create
        - Read: Clase que hereda de la interfaz Read
        - Update: Clase que hereda de la interfaz Update
    '''
    
    def __init__(self,):
        self.__type_model = EventModel

    def create(self, model: db.Model):
        db.session.add(model)
        db.session.commit()
        return model

    def update(self, model: db.Model) -> db.Model:
        db.session.merge(model)
        db.session.commit()
        return model 
    
    def delete(self, model: db.Model):
        db.session.delete(model)
        db.session.commit()

    def delete_by_id(self, id: int):
        db.session.query(self.__type_model).filter_by(id=id).delete()
        db.session.commit() 

    def find_all(self):
        model = db.session.query(self.__type_model).all()
        return model

    def find_by_id(self, id: int) -> db.Model:
        model = db.session.query(self.__type_model).filter_by(id=id).first()
        return model