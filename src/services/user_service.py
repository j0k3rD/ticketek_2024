from src.repositories import UserRepository
from src.services.services import Service

repository = UserRepository()

class UserService(Service):
    '''
    Clase que representa el servicio de la entidad User

    param:
        - Service: Clase que hereda de la interfaz Service
    '''

    def add(self, model):
        return repository.create(model)
        
    def get_all(self):
        return repository.find_all()

    def get_by_id(self, id):
        return repository.find_by_id(id = id)