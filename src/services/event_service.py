from src.repositories import EventRepository
from src.services.services import Service

repository = EventRepository()

class EventService(Service):
    '''
    Clase que representa el servicio de la entidad Event

    param:
        - Service: Clase que hereda de la interfaz Service
    '''

    def add(self, model):
        return repository.create(model)
        
    def get_all(self):
        return repository.find_all()

    def get_by_id(self, id):
        return repository.find_by_id(id = id)